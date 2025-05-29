import streamlit as st
st.set_page_config(
    page_title="유심 교체 대기 등록",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Git/Streamlit 접근 차단 CSS 및 다크모드 최적화
st.markdown("""
    <style>
    /* Git/Streamlit 하단 링크 숨기기 (master 권한자 외) */
    .stAppDeployButton,
    footer,
    .stDeployButton,
    #MainMenu,
    header[data-testid="stHeader"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 다크모드 최적화 */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #0e1117 !important;
        }
        
        .stSelectbox > div > div {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        .stTextInput > div > div > input {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        .stButton > button {
            background-color: #262730 !important;
            color: #fafafa !important;
            border: 1px solid #4a4a4a !important;
        }
        
        .stButton > button:hover {
            background-color: #3a3a3a !important;
            border: 1px solid #6a6a6a !important;
        }
        
        .stInfo {
            background-color: #1a1a2e !important;
            color: #fafafa !important;
        }
        
        .stWarning {
            background-color: #2e1a1a !important;
            color: #fafafa !important;
        }
        
        .stSuccess {
            background-color: #1a2e1a !important;
            color: #fafafa !important;
        }
        
        .stError {
            background-color: #3d1a1a !important;
            color: #fafafa !important;
        }
        
        /* 고객 카드 다크모드 최적화 */
        div[style*="background-color:#fff3cd"] {
            background-color: #3d3d1a !important;
            color: #fafafa !important;
        }
        
        div[style*="background-color:#d1ecf1"] {
            background-color: #1a3d3d !important;
            color: #fafafa !important;
        }
        
        div[style*="background-color:#d4edda"] {
            background-color: #1a3d1a !important;
            color: #fafafa !important;
        }
    }
    
    /* 라이트모드에서도 접근 제한 유지 */
    .stAppDeployButton,
    footer,
    .stDeployButton,
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

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

    def get_all_stores(self):
        """모든 매장 정보 가져오기"""
        sheet = self.workbook.worksheet("stores")
        all_values = sheet.get_all_records()
        return all_values
    
    def get_teams(self):
        """모든 팀 목록 가져오기"""
        stores = self.get_all_stores()
        teams = list(set([store['team'] for store in stores if store.get('team')]))
        return sorted(teams)
    
    def get_stores_by_team(self, team):
        """특정 팀의 매장들 가져오기"""
        stores = self.get_all_stores()
        team_stores = [store for store in stores if store.get('team') == team]
        return team_stores
    
    def get_store_by_name(self, store_name):
        """매장명으로 매장 정보 찾기"""
        stores = self.get_all_stores()
        for store in stores:
            if store.get('store_name') == store_name:
                return store
        return None
    
    def set_store_admin_by_name(self, store_name, admin_id, admin_pw):
        """매장명으로 관리자 정보 설정"""
        sheet = self.workbook.worksheet("stores")
        all_values = sheet.get_all_values()
        headers = all_values[0]
        
        try:
            store_name_idx = headers.index("store_name")
            admin_id_idx = headers.index("admin_id")
            admin_pw_idx = headers.index("admin_pw")
        except ValueError:
            return False
            
        for i, row in enumerate(all_values[1:], start=2):
            if row[store_name_idx] == store_name:
                sheet.update_cell(i, admin_id_idx + 1, admin_id)
                sheet.update_cell(i, admin_pw_idx + 1, admin_pw)
                return True
        return False

# 전산 담당자 화면

# show_admin_view 함수 수정
def show_admin_view(sheets_manager, store_code=None):
    import io
    from streamlit import download_button
    
    # 자동 새로고침 및 다크모드 최적화
    st.markdown("""
        <script>
        setTimeout(function() {
            window.location.reload();
        }, 30000);
        </script>
        <style>
        /* 다크모드에서 고객 카드 색상 최적화 */
        @media (prefers-color-scheme: dark) {
            .customer-card-waiting {
                background-color: #3d3d1a !important;
                color: #fafafa !important;
            }
            .customer-card-processing {
                background-color: #1a3d3d !important;
                color: #fafafa !important;
            }
            .customer-card-done {
                background-color: #1a3d1a !important;
                color: #fafafa !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.subheader("💻 전산 담당자용 고객 목록")

    store_code = store_code or st.session_state.get("selected_store_code")
    if not store_code:
        st.warning("❗ 먼저 '로그인' 탭에서 매장을 선택해주세요.")
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

    # 화면에는 대기, 처리중인 고객만 표시 (다크모드 최적화)
    for customer in filtered_for_display:
        with st.container():
            status = customer['status']
            # 다크모드를 고려한 색상 설정
            if status == '대기':
                bg_color = "#fff3cd"
                css_class = "customer-card-waiting"
            elif status == '처리중':
                bg_color = "#d1ecf1" 
                css_class = "customer-card-processing"
            else:
                bg_color = "#d4edda"
                css_class = "customer-card-done"
                
            st.markdown(f"""
                <div class="{css_class}" style='background-color:{bg_color}; padding:10px; border-radius:8px; margin-bottom:10px;'>
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
    # 다크모드 최적화 CSS 추가
    st.markdown("""
        <style>
        input[type="text"], input[type="password"] {
            font-size: 24px !important;
        }
        label { 
            font-size: 20px !important; 
        }
        
        /* 다크모드에서 입력 필드 최적화 */
        @media (prefers-color-scheme: dark) {
            .stTextInput > div > div > input {
                background-color: #262730 !important;
                color: #fafafa !important;
                border: 2px solid #4a4a4a !important;
                font-size: 24px !important;
            }
            
            .stTextInput > label {
                color: #fafafa !important;
                font-size: 20px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    from Home import show_input_screen, get_store_name

    store_code = store_code or st.session_state.get("selected_store_code", "STORE001")
    store_name = st.session_state.get("selected_store_name", get_store_name(store_code, sheets_manager))
    show_input_screen(store_name, store_code)

# 수정된 로그인 화면
def show_login(sheets_manager):
    if 'selected_store_name' in st.session_state:
        st.success(f"✅ 로그인 성공! 왼쪽 사이드바 메뉴에서 선택해주세요~ {st.session_state['selected_store_name']}")
        return
        
    st.subheader("🔐 매장 관리자 로그인")
    
    try:
        # 팀 목록 가져오기
        teams = sheets_manager.get_teams()
        
        if not teams:
            st.error("❌ 등록된 팀이 없습니다.")
            return
            
        # 팀 선택
        selected_team = st.selectbox("👥 팀 선택", ["팀을 선택하세요..."] + teams)
        
        if selected_team == "팀을 선택하세요...":
            return
            
        # 선택된 팀의 모든 매장들 가져오기
        team_stores = sheets_manager.get_stores_by_team(selected_team)
        
        if not team_stores:
            st.warning(f"❗ {selected_team}에 등록된 매장이 없습니다.")
            return
            
        # 관리자 등록된 매장과 미등록된 매장 분리
        registered_stores = [store for store in team_stores if store.get('admin_id', '').strip()]
        
        # 관리자가 등록된 매장이 없는 경우 - 관리자 등록 유도
        if not registered_stores:
            st.warning(f"❗ {selected_team}에 관리자가 등록된 매장이 없습니다.")
            st.markdown("### 🎯 관리자 등록이 필요합니다")
            st.info("1️⃣ 상단의 '관리자 등록' 탭으로 이동하세요")
            st.info("2️⃣ 매장을 선택하고 관리자 정보를 등록하세요")
            st.info("3️⃣ 등록 완료 후 이 화면에서 로그인하세요")
            return
            
        # 로그인할 매장 선택
        store_names = [store['store_name'] for store in registered_stores]
        selected_store_name = st.selectbox("🏪 매장 선택", ["매장을 선택하세요..."] + store_names)
        
        if selected_store_name == "매장을 선택하세요...":
            return
            
        # 선택된 매장 정보 표시
        selected_store = next(store for store in registered_stores if store['store_name'] == selected_store_name)
        st.info(f"📍 선택된 매장: **{selected_store['store_name']}** ({selected_store['team']})")
        
        admin_id = st.text_input("👤 관리자 ID")
        admin_pw = st.text_input("🔒 비밀번호", type="password")

        if st.button("🔓 로그인"):
            store = sheets_manager.get_store_by_name(selected_store_name)

            if not store:
                st.error("❌ 매장 정보를 찾을 수 없습니다.")
                return

            if store.get("admin_id", "").strip() == admin_id.strip() and store.get("admin_pw", "").strip() == admin_pw.strip():
                st.session_state['selected_store_code'] = store['store_code']
                st.session_state['selected_store_name'] = store['store_name']
                st.success(f"✅ {store['store_name']} 로그인 성공!")
                st.rerun()
            else:
                st.error("❌ 관리자 ID 또는 비밀번호가 올바르지 않습니다.")
                
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

# 수정된 관리자 설정 화면
def show_store_admin_settings(sheets_manager):
    st.subheader("🆕 관리자 등록 (최초 1회)")
    
    try:
        # 팀 목록 가져오기
        teams = sheets_manager.get_teams()
        
        if not teams:
            st.error("❌ 등록된 팀이 없습니다.")
            return
            
        # 팀 선택
        selected_team = st.selectbox("👥 팀 선택", ["팀을 선택하세요..."] + teams)
        
        if selected_team == "팀을 선택하세요...":
            return
            
        # 선택된 팀의 매장들 가져오기
        team_stores = sheets_manager.get_stores_by_team(selected_team)
        
        if not team_stores:
            st.warning(f"❗ {selected_team}에 등록된 매장이 없습니다.")
            return
            
        # 매장 선택 (관리자가 미등록된 매장만 표시)
        available_stores = [store for store in team_stores if not store.get('admin_id', '').strip()]
        
        if not available_stores:
            st.info(f"ℹ️ {selected_team}의 모든 매장에 관리자가 이미 등록되어 있습니다.")
            return
            
        store_names = [store['store_name'] for store in available_stores]
        selected_store_name = st.selectbox("🏪 매장 선택", ["매장을 선택하세요..."] + store_names)
        
        if selected_store_name == "매장을 선택하세요...":
            return
            
        # 선택된 매장 정보 표시
        selected_store = next(store for store in available_stores if store['store_name'] == selected_store_name)
        st.info(f"📍 선택된 매장: **{selected_store['store_name']}** ({selected_store['team']})")
        
        # 관리자 정보 입력
        admin_id = st.text_input("👤 관리자 ID")
        admin_pw = st.text_input("🔒 관리자 비밀번호", type="password")
        admin_pw_confirm = st.text_input("🔒 비밀번호 확인", type="password")
        
        if admin_pw and admin_pw != admin_pw_confirm:
            st.error("❌ 비밀번호가 일치하지 않습니다.")
            
        if st.button("💾 관리자 등록"):
            if not admin_id.strip():
                st.error("❌ 관리자 ID를 입력해주세요.")
                return
                
            if not admin_pw.strip():
                st.error("❌ 비밀번호를 입력해주세요.")
                return
                
            if admin_pw != admin_pw_confirm:
                st.error("❌ 비밀번호가 일치하지 않습니다.")
                return
                
            success = sheets_manager.set_store_admin_by_name(selected_store_name, admin_id, admin_pw)
            if success:
                st.session_state['selected_store_code'] = selected_store['store_code']
                st.session_state['selected_store_name'] = selected_store['store_name']
                st.success(f"✅ {selected_store_name} 관리자 등록이 완료되었습니다!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ 관리자 등록에 실패했습니다.")
                
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

# 로그아웃 기능 추가
def show_logout_button():
    if 'selected_store_name' in st.session_state:
        if st.button("🚪 로그아웃"):
            # 세션 상태 초기화
            if 'selected_store_code' in st.session_state:
                del st.session_state['selected_store_code']
            if 'selected_store_name' in st.session_state:
                del st.session_state['selected_store_name']
            st.success("✅ 로그아웃되었습니다.")
            st.rerun()

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
            show_logout_button()  # 로그아웃 버튼 추가
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
