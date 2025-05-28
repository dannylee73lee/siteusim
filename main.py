import streamlit as st
st.set_page_config(
    page_title="유심 교체 대기 등록",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from datetime import datetime
import pandas as pd
import time
from Home import init_google_sheets

# Google Sheets 데이터 처리 클래스

def get_store_by_code(sheet, store_code):
    all_values = sheet.get_all_records()
    for row in all_values:
        if row.get("store_code") == store_code:
            return row
    return None

class SheetsManager:
    def __init__(self, workbook):
        self.workbook = workbook

    def get_customers(self):
        sheet = self.workbook.worksheet("customers")
        all_values = sheet.get_all_values()
        headers = all_values[0]
        data = []
        for row in all_values[1:]:
            if not row or len(row) < 5:
                continue
            record = dict(zip(headers, row))
            try:
                record['registered_time'] = datetime.strptime(record['registered_time'], "%y-%m-%d, %I:%M %p")
            except:
                record['registered_time'] = datetime.now()
            data.append(record)
        return data

    def update_customer_status(self, customer_id, new_status):
        sheet = self.workbook.worksheet("customers")
        all_values = sheet.get_all_values()
        headers = all_values[0]
        for i, row in enumerate(all_values[1:], start=2):
            if row[0] == str(customer_id):
                sheet.update_cell(i, headers.index('status') + 1, new_status)
                break

    def get_store_by_code(self, store_code):
        sheet = self.workbook.worksheet("stores")
        return get_store_by_code(sheet, store_code)

    def set_store_admin(self, store_code, admin_id, admin_pw):
        sheet = self.workbook.worksheet("stores")
        all_values = sheet.get_all_values()
        headers = all_values[0]
        try:
            store_code_idx = headers.index("store_code")
            admin_id_idx = headers.index("admin_id")
            admin_pw_idx = headers.index("admin_pw")
        except ValueError:
            return False
        for i, row in enumerate(all_values[1:], start=2):
            if row[store_code_idx] == store_code:
                sheet.update_cell(i, admin_id_idx + 1, admin_id)
                sheet.update_cell(i, admin_pw_idx + 1, admin_pw)
                return True
        return False

# 전산 담당자 화면

# show_admin_view 함수 수정
def show_admin_view(sheets_manager, store_code=None):
    import io
    from streamlit import download_button
    # 자동 새로고침 (30초 간격)
    st.markdown("""
        <script>
        setTimeout(function() {
            window.location.reload();
        }, 30000);
        </script>
    """, unsafe_allow_html=True)
    st.subheader("💻 전산 담당자용 고객 목록")

    store_code = store_code or st.session_state.get("selected_store_code")
    if not store_code:
        st.warning("❗ 먼저 '관리자 설정' 탭에서 매장을 선택해주세요.")
        return

    # 전체 고객 데이터 가져오기 (모든 상태 포함)
    all_customers = [c for c in sheets_manager.get_customers() if c.get('store_code') == store_code]
    
    # 화면 표시용 (대기, 처리중만)
    filtered_for_display = [c for c in all_customers if c['status'] in ['대기', '처리중']]

    if st.button("🔄 새로고침"):
        st.rerun()

    st.markdown("---")
    st.caption("테이블에서 직접 상태를 변경하세요:")

    # 엑셀 다운로드 버튼 - 전체 데이터로 변경
    if all_customers:
        df_all = pd.DataFrame(all_customers)
        df_all['registered_time'] = pd.to_datetime(df_all['registered_time'], errors='coerce')
        df_all = df_all.sort_values(by='registered_time')
        
        # 상태별 개수 표시
        status_counts = df_all['status'].value_counts()
        st.info(f"📊 전체 현황: 대기 {status_counts.get('대기', 0)}명 | 처리중 {status_counts.get('처리중', 0)}명 | 완료 {status_counts.get('완료', 0)}명")
        
        excel_buffer = io.BytesIO()
        writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')
        df_all.to_excel(writer, index=False, sheet_name='전체 고객 목록')
        writer.close()
        
        st.download_button(
            label="📥 전체 고객 엑셀 다운로드 (대기+처리중+완료)",
            data=excel_buffer.getvalue(),
            file_name=f"전체_고객_목록_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("다운로드할 데이터가 없습니다.")

    # 화면에는 대기, 처리중인 고객만 표시
    for customer in filtered_for_display:
        with st.container():
            status = customer['status']
            bg_color = "#fff3cd" if status == '대기' else ("#d1ecf1" if status == '처리중' else ("#d4edda" if status == '완료' else "#ffffff"))
            st.markdown(f"""
                <div style='background-color:{bg_color}; padding:10px; border-radius:8px; margin-bottom:10px;'>
                    <div style='display:flex; align-items:center; justify-content:space-between;'>
                        <div style='flex:1;'><strong>ID:</strong> {customer['id']}</div>
                        <div style='flex:2;'><strong>이름:</strong> {customer['name']}</div>
                        <div style='flex:2;'><strong>전화:</strong> {customer['phone']}</div>
                        <div style='flex:2;'><strong>상태:</strong> {customer['status']}</div>
                        <div style='flex:2;'>""", unsafe_allow_html=True)

            if customer['status'] == '대기':
                if st.button(f"▶ 처리 시작 ({customer['id']})", key=f"start_{customer['id']}"):
                    sheets_manager.update_customer_status(customer['id'], '처리중')
                    st.success(f"ID {customer['id']} → 처리중")
                    st.rerun()
            elif customer['status'] == '처리중':
                if st.button(f"✅ 완료 처리 ({customer['id']})", key=f"done_{customer['id']}"):
                    sheets_manager.update_customer_status(customer['id'], '완료')
                    st.success(f"ID {customer['id']} → 완료")
                    st.rerun()

            st.markdown("""</div></div>""", unsafe_allow_html=True)

# 고객 등록 화면 (기존 코드와 연동)
def show_customer_view(sheets_manager, store_code=None):
    st.markdown("""
        <style>
        input[type="text"], input[type="password"] {
            font-size: 24px !important;
        }
        label { font-size: 20px !important; }
        </style>
    """, unsafe_allow_html=True)
    from Home import show_input_screen, get_store_name

    store_code = store_code or st.session_state.get("selected_store_code", "STORE001")
    store_name = st.session_state.get("selected_store_name", get_store_name(store_code, sheets_manager))
    show_input_screen(store_name, store_code)

# 로그인 화면

def show_login(sheets_manager):
    if 'selected_store_name' in st.session_state:
        st.success(f"✅ 이미 로그인됨: {st.session_state['selected_store_name']}")
        return
    st.subheader("🔐 매장 관리자 로그인")
    store_code = st.text_input("🏪 매장 코드")
    admin_id = st.text_input("👤 관리자 ID")
    admin_pw = st.text_input("🔒 비밀번호", type="password")

    if st.button("🔓 로그인"):
        store = sheets_manager.get_store_by_code(store_code)

        if not store:
            st.error("❌ 매장 코드가 유효하지 않습니다.")
            return

        st.write("📋 입력값:", store_code, admin_id, admin_pw)
        st.write("📋 시트값:", store.get("store_code"), store.get("admin_id"), store.get("admin_pw"))

        if store.get("admin_id", "").strip() == admin_id.strip() and store.get("admin_pw", "").strip() == admin_pw.strip():
            st.session_state['selected_store_code'] = store_code
            st.session_state['selected_store_name'] = store['store_name']
            st.success(f"{store['store_name']} 로그인 성공")
            st.rerun()
        else:
            st.error("❌ 로그인 정보가 올바르지 않습니다.")


# 관리자 설정 화면
def show_store_admin_settings(sheets_manager):
    st.subheader("🆕 관리자 등록 (최초 1회)")
    store_code = st.text_input("🏪 매장 코드")

    if store_code:
        store = sheets_manager.get_store_by_code(store_code)
        if store:
            st.markdown(f"**{store['store_name']}** ({store_code})")
            if store.get("admin_id"):
                st.info("이미 등록된 매장입니다. 로그인 탭을 이용하세요.")
                return

            admin_id = st.text_input("👤 관리자 ID")
            admin_pw = st.text_input("🔒 관리자 비밀번호", type="password")

            if st.button("💾 저장"):
                success = sheets_manager.set_store_admin(store_code, admin_id, admin_pw)
                if success:
                    st.session_state['selected_store_code'] = store_code
                    st.session_state['selected_store_name'] = store['store_name']
                    st.success("관리자 정보가 저장되었습니다.")
                    st.rerun()
                else:
                    st.error("저장 실패: 해당 매장을 찾을 수 없습니다.")
        else:
            st.warning("유효한 매장 코드가 아닙니다.")

# 메인 함수
def main():
    workbook, client = init_google_sheets()
    if workbook is None:
        st.error("📛 Google Sheets 연결 오류")
        return

    sheets_manager = SheetsManager(workbook)

    with st.sidebar:
        if 'selected_store_name' in st.session_state:
            st.markdown(f"**🔓 로그인됨:** `{st.session_state['selected_store_name']}`")
        else:
            st.markdown("🔒 로그인되지 않음")
        tab = st.radio("모드 선택", ["로그인", "고객 등록", "전산 처리", "관리자 등록"])

    if tab == "로그인":
        show_login(sheets_manager)
    elif tab == "고객 등록":
        show_customer_view(sheets_manager)
    elif tab == "전산 처리":
        show_admin_view(sheets_manager)
    elif tab == "관리자 등록":
        show_store_admin_settings(sheets_manager)

if __name__ == '__main__':
    main()
