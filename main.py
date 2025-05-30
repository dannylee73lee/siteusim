import streamlit as st

# robots.txt 처리 - 더 안전한 방법
try:
    if st.query_params.get('robots') == 'txt':
        st.text("""User-agent: *
Disallow: /""")
        st.stop()
except:
    pass

st.set_page_config(
    page_title="유심 교체 대기 등록",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 검색엔진 차단 메타 태그 및 referrer 차단
st.markdown("""
    <meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
    <meta name="googlebot" content="noindex, nofollow">
    <meta name="bingbot" content="noindex, nofollow">
    
    <script>
    // 검색엔진에서 온 방문자 차단
    (function() {
        var referrer = document.referrer.toLowerCase();
        var searchEngines = ['google.', 'bing.', 'yahoo.', 'duckduckgo.', 'search.'];
        
        for (var i = 0; i < searchEngines.length; i++) {
            // 검색엔진에서 온 경우 완전히 차단
            if (referrer.includes(searchEngines[i])) {
                // GitHub로도 가지 못하게 완전 차단
                document.head.innerHTML = '<title>404 Not Found</title>';
                document.body.innerHTML = '<div style="text-align:center;margin-top:100px;font-family:Arial;"><h1>404</h1><h2>Page Not Found</h2></div>';
                
                // 히스토리도 조작해서 뒤로가기 방지
                history.replaceState(null, '', '/404');
                
                return false;
            }
        }
    })();
    </script>
    
    <style>
    /* Git/Streamlit 하단 링크 숨기기 - 강화된 버전 */
    .stAppDeployButton,
    footer,
    .stDeployButton,
    #MainMenu,
    header[data-testid="stHeader"],
    .stAppHeader,
    .stToolbar,
    .viewerBadge_container__r5tak,
    .viewerBadge_link__qRIco,
    footer[data-testid="stDecoration"],
    .stDecoration,
    [data-testid="stDecoration"],
    .css-1rs6os.edgvbvh3,
    .css-10trblm.e16nr0p30,
    .css-1y0tads.eczjsme18,
    .streamlit-footer,
    a[href*="streamlit.io"],
    a[href*="github.com/streamlit"],
    .github-corner,
    div[class*="viewerBadge"],
    div[data-testid="ViewerBadge"],
    .ViewerBadge,
    [data-testid="toolbarDecorationContainer"] {
        visibility: hidden !important;
        display: none !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
        left: -9999px !important;
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
    
    /* 라이트모드에서도 접근 제한 유지 - 강화 버전 */
    .stAppDeployButton,
    footer,
    .stDeployButton,
    #MainMenu,
    .stAppHeader,
    .stToolbar,
    .viewerBadge_container__r5tak,
    .viewerBadge_link__qRIco,
    footer[data-testid="stDecoration"],
    .stDecoration,
    [data-testid="stDecoration"],
    .css-1rs6os.edgvbvh3,
    .css-10trblm.e16nr0p30,
    .css-1y0tads.eczjsme18,
    .streamlit-footer,
    a[href*="streamlit.io"],
    a[href*="github.com/streamlit"],
    .github-corner,
    div[class*="viewerBadge"],
    div[data-testid="ViewerBadge"],
    .ViewerBadge,
    [data-testid="toolbarDecorationContainer"] {
        visibility: hidden !important;
        display: none !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }
    
    /* 추가적인 Streamlit 브랜딩 요소 제거 */
    .css-1dp5vir {
        display: none !important;
    }
    
    /* 'Made with Streamlit' 텍스트 숨기기 */
    .css-cio0fd {
        visibility: hidden !important;
    }
    
    /* GitHub 아이콘이나 기타 외부 링크 제거 */
    .css-1aumxhk {
        display: none !important;
    }
    </style>
    <script>
    // JavaScript로 동적으로 Streamlit 브랜딩 요소 제거
    function hideStreamlitElements() {
        // 일반적인 Streamlit 브랜딩 요소들
        const selectors = [
            'footer',
            '.stAppDeployButton',
            '.stDeployButton', 
            '#MainMenu',
            '.stAppHeader',
            '.stToolbar',
            '[data-testid="stDecoration"]',
            '[data-testid="ViewerBadge"]',
            '[data-testid="toolbarDecorationContainer"]',
            'a[href*="streamlit.io"]',
            'a[href*="github.com/streamlit"]',
            '.github-corner',
            'div[class*="viewerBadge"]'
        ];
        
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                element.style.display = 'none';
                element.style.visibility = 'hidden';
                element.style.opacity = '0';
                element.style.height = '0';
                element.style.width = '0';
                element.style.position = 'absolute';
                element.style.left = '-9999px';
            });
        });
        
        // 텍스트 기반으로 'Made with Streamlit' 등 제거
        const allElements = document.querySelectorAll('*');
        allElements.forEach(element => {
            if (element.innerText && 
                (element.innerText.includes('Made with Streamlit') || 
                 element.innerText.includes('Streamlit') ||
                 element.innerText.includes('GitHub'))) {
                if (element.tagName === 'A' || element.closest('a')) {
                    element.style.display = 'none';
                }
            }
        });
    }
    
    // 페이지 로드 시 실행
    document.addEventListener('DOMContentLoaded', hideStreamlitElements);
    
    // MutationObserver로 동적 생성 요소도 감지하여 제거
    const observer = new MutationObserver(function(mutations) {
        hideStreamlitElements();
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    // 주기적으로도 체크 (1초마다)
    setInterval(hideStreamlitElements, 1000);
    </script>
""", unsafe_allow_html=True)

from datetime import datetime
import pandas as pd
import time
import io
from Home import init_google_sheets, SheetsManager, get_store_name, mask_phone

# API 호출 최적화를 위한 에러 핸들링
def safe_api_call(func, *args, **kwargs):
    """API 호출 시 429 에러 처리"""
    max_retries = 3
    retry_delay = 2  # 초
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "429" in str(e) or "Quota exceeded" in str(e):
                if attempt < max_retries - 1:
                    st.warning(f"⏳ API 한도 초과. {retry_delay}초 후 재시도... ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 지수적 백오프
                    continue
                else:
                    st.error("❌ API 호출 한도 초과. 잠시 후 다시 시도해주세요.")
                    return None
            else:
                st.error(f"❌ 오류 발생: {str(e)}")
                return None
    return None

# 권한 확인 함수
def check_admin_permission():
    """관리자 권한 확인"""
    if st.session_state.get('user_level') != 'admin':
        st.error("❌ 관리자 권한이 필요합니다.")
        st.info("💡 관리자 로그인 후 이용해주세요.")
        return False
    return True

# 전산 담당자 화면
def show_admin_view(sheets_manager, store_code=None):
    # 관리자 권한 체크
    if not check_admin_permission():
        return
    
    # 자동 새로고침 및 다크모드 최적화
    st.markdown("""
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

    # 디버깅 정보 표시
    st.info(f"🔍 현재 매장 코드: {store_code}")
    
    # 전체 고객 데이터 가져오기 (안전한 API 호출)
    all_customers_raw = safe_api_call(sheets_manager.get_customers)
    
    if all_customers_raw is None:
        st.error("❌ 고객 데이터를 불러올 수 없습니다.")
        return
    
    # 현재 매장의 고객만 필터링
    all_customers = [c for c in all_customers_raw if c.get('store_code') == store_code]
    
    # 디버깅: 전체 데이터 확인
    st.expander("🔍 디버깅 정보", expanded=False).write({
        "전체 고객 수": len(all_customers_raw),
        "현재 매장 고객 수": len(all_customers),
        "매장 코드": store_code,
        "샘플 데이터": all_customers_raw[:3] if all_customers_raw else "없음"
    })
    
    # 화면 표시용 (대기, 처리중만)
    filtered_for_display = [c for c in all_customers if c['status'] in ['대기', '처리중']]

    if st.button("🔄 새로고침"):
        # 캐시 클리어
        st.cache_data.clear()
        st.rerun()

    st.markdown("---")
    
    # 고객이 없는 경우 안내
    if not all_customers:
        st.info("📝 아직 등록된 고객이 없습니다.")
        st.markdown("### 💡 확인사항")
        st.markdown("1. 고객 등록이 정상적으로 완료되었는지 확인")
        st.markdown("2. 매장 코드가 올바른지 확인")
        st.markdown("3. Google Sheets 연결 상태 확인")
        return
    
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
    
    # 대기/처리중 고객이 없는 경우
    if not filtered_for_display:
        st.warning("⏳ 현재 대기중이거나 처리중인 고객이 없습니다.")
        if all_customers:
            completed_count = len([c for c in all_customers if c['status'] == '완료'])
            st.info(f"✅ 완료된 고객: {completed_count}명")
        return

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
            
            # 전산 담당자 화면에서는 전화번호 마스킹 없음
            displayed_phone = mask_phone(customer['phone'], is_admin_view=True)
                
            st.markdown(f"""
                <div class="{css_class}" style='background-color:{bg_color}; padding:10px; border-radius:8px; margin-bottom:10px;'>
                    <div style='display:flex; align-items:center; justify-content:space-between;'>
                        <div style='flex:1;'><strong>ID:</strong> {customer['id']}</div>
                        <div style='flex:2;'><strong>이름:</strong> {customer['name']}</div>
                        <div style='flex:2;'><strong>전화:</strong> {displayed_phone}</div>
                        <div style='flex:2;'><strong>상태:</strong> {customer['status']}</div>
                        <div style='flex:2;'>""", unsafe_allow_html=True)

            if customer['status'] == '대기':
                if st.button(f"▶ 처리 시작 ({customer['id']})", key=f"start_{customer['id']}"):
                    success = safe_api_call(sheets_manager.update_customer_status, customer['id'], '처리중')
                    if success is not None:
                        st.success(f"ID {customer['id']} → 처리중")
                        st.cache_data.clear()  # 캐시 클리어
                        st.rerun()
            elif customer['status'] == '처리중':
                if st.button(f"✅ 완료 처리 ({customer['id']})", key=f"done_{customer['id']}"):
                    success = safe_api_call(sheets_manager.update_customer_status, customer['id'], '완료')
                    if success is not None:
                        st.success(f"ID {customer['id']} → 완료")
                        st.cache_data.clear()  # 캐시 클리어
                        st.rerun()

            st.markdown("""</div></div>""", unsafe_allow_html=True)

# 고객 등록 화면 (Home.py의 함수 호출)
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
    
    from Home import show_input_screen
    
    store_code = store_code or st.session_state.get("selected_store_code", "STORE001")
    store_name = st.session_state.get("selected_store_name", get_store_name(store_code, sheets_manager))
    show_input_screen(store_name, store_code)

# 수정된 로그인 화면
def show_login(sheets_manager):
    if 'selected_store_name' in st.session_state:
        user_level = st.session_state.get('user_level', 'customer')
        level_text = "관리자" if user_level == 'admin' else "고객"
        st.success(f"✅ {level_text} 로그인 성공! 왼쪽 사이드바 메뉴에서 선택해주세요~ {st.session_state['selected_store_name']}")
        return
        
    st.subheader("🔐 로그인")
    
    # 접속 유형 선택
    access_type = st.selectbox("접속 유형", ["접속 유형을 선택하세요", "고객", "관리자"])
    
    if access_type == "접속 유형을 선택하세요":
        return
    elif access_type == "고객":
        show_customer_login(sheets_manager)
    elif access_type == "관리자":
        show_admin_login(sheets_manager)

def show_customer_login(sheets_manager):
    """고객 로그인 (user_id, user_pw 확인)"""
    st.markdown("### 👥 고객 접속")
    st.info("💡 고객 등록 화면만 이용 가능합니다")
    
    try:
        # 팀 목록 가져오기 (안전한 API 호출)
        teams = safe_api_call(sheets_manager.get_teams)
        
        if teams is None:  # API 오류 발생
            return
        
        if not teams:
            st.error("❌ 등록된 팀이 없습니다.")
            return
            
        # 팀 선택
        selected_team = st.selectbox("👥 팀 선택", ["팀을 선택하세요..."] + teams, key="customer_team")
        
        if selected_team == "팀을 선택하세요...":
            return
            
        # 선택된 팀의 매장들 가져오기 (안전한 API 호출)
        team_stores = safe_api_call(sheets_manager.get_stores_by_team, selected_team)
        
        if team_stores is None:  # API 오류 발생
            return
        
        if not team_stores:
            st.warning(f"❗ {selected_team}에 등록된 매장이 없습니다.")
            return
            
        # 고객 계정이 등록된 매장만 필터링
        customer_enabled_stores = [store for store in team_stores if store.get('user_id', '').strip()]
        
        if not customer_enabled_stores:
            st.warning(f"❗ {selected_team}에 고객 계정이 등록된 매장이 없습니다.")
            st.markdown("### 🎯 고객 계정 등록이 필요합니다")
            st.info("관리자에게 고객 계정(user_id, user_pw) 등록을 요청하세요")
            return
            
        # 매장 선택
        store_names = [store['store_name'] for store in customer_enabled_stores]
        selected_store_name = st.selectbox("🏪 매장 선택", ["매장을 선택하세요..."] + store_names, key="customer_store")
        
        if selected_store_name == "매장을 선택하세요...":
            return
            
        # 선택된 매장 정보 표시
        selected_store = next(store for store in customer_enabled_stores if store['store_name'] == selected_store_name)
        st.info(f"📍 선택된 매장: **{selected_store['store_name']}** ({selected_store['team']})")
        
        # 고객 인증 정보 입력
        user_id = st.text_input("👤 사용자 ID", key="customer_user_id")
        user_pw = st.text_input("🔒 비밀번호", type="password", key="customer_user_pw")
        
        if st.button("🚀 고객 등록 시작", key="customer_start"):
            # 고객 계정 인증
            if selected_store.get("user_id", "").strip() == user_id.strip() and selected_store.get("user_pw", "").strip() == user_pw.strip():
                st.session_state['selected_store_code'] = selected_store['store_code']
                st.session_state['selected_store_name'] = selected_store['store_name']
                st.session_state['user_level'] = 'customer'  # 고객 권한 설정
                st.success(f"✅ {selected_store['store_name']} 고객 모드로 접속되었습니다!")
                st.rerun()
            else:
                st.error("❌ 사용자 ID 또는 비밀번호가 올바르지 않습니다.")
            
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

def show_admin_login(sheets_manager):
    """관리자 로그인"""
    st.markdown("### 🔐 관리자 로그인")
    
    try:
        # 팀 목록 가져오기
        teams = sheets_manager.get_teams()
        
        if not teams:
            st.error("❌ 등록된 팀이 없습니다.")
            return
            
        # 팀 선택
        selected_team = st.selectbox("👥 팀 선택", ["팀을 선택하세요..."] + teams, key="admin_team")
        
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
        selected_store_name = st.selectbox("🏪 매장 선택", ["매장을 선택하세요..."] + store_names, key="admin_store")
        
        if selected_store_name == "매장을 선택하세요...":
            return
            
        # 선택된 매장 정보 표시
        selected_store = next(store for store in registered_stores if store['store_name'] == selected_store_name)
        st.info(f"📍 선택된 매장: **{selected_store['store_name']}** ({selected_store['team']})")
        
        admin_id = st.text_input("👤 관리자 ID", key="admin_id_input")
        admin_pw = st.text_input("🔒 비밀번호", type="password", key="admin_pw_input")

        if st.button("🔓 관리자 로그인", key="admin_login_btn"):
            store = sheets_manager.get_store_by_name(selected_store_name)

            if not store:
                st.error("❌ 매장 정보를 찾을 수 없습니다.")
                return

            if store.get("admin_id", "").strip() == admin_id.strip() and store.get("admin_pw", "").strip() == admin_pw.strip():
                st.session_state['selected_store_code'] = store['store_code']
                st.session_state['selected_store_name'] = store['store_name']
                st.session_state['user_level'] = 'admin'  # 관리자 권한 설정
                st.success(f"✅ {store['store_name']} 관리자 로그인 성공!")
                st.rerun()
            else:
                st.error("❌ 관리자 ID 또는 비밀번호가 올바르지 않습니다.")
                
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

# 수정된 관리자 설정 화면
def show_store_admin_settings(sheets_manager):
    st.subheader("🆕 계정 등록 (최초 1회)")
    
    # 탭으로 관리자/고객 계정 등록 구분
    tab1, tab2 = st.tabs(["👨‍💼 관리자 계정", "👥 고객 계정"])
    
    with tab1:
        show_admin_account_setup(sheets_manager)
    
    with tab2:
        show_customer_account_setup(sheets_manager)

def show_admin_account_setup(sheets_manager):
    """관리자 계정 설정"""
    st.markdown("### 👨‍💼 관리자 계정 등록")
    
    try:
        # 팀 목록 가져오기
        teams = sheets_manager.get_teams()
        
        if not teams:
            st.error("❌ 등록된 팀이 없습니다.")
            return
            
        # 팀 선택
        selected_team = st.selectbox("👥 팀 선택", ["팀을 선택하세요..."] + teams, key="admin_settings_team")
        
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
        selected_store_name = st.selectbox("🏪 매장 선택", ["매장을 선택하세요..."] + store_names, key="admin_settings_store")
        
        if selected_store_name == "매장을 선택하세요...":
            return
            
        # 선택된 매장 정보 표시
        selected_store = next(store for store in available_stores if store['store_name'] == selected_store_name)
        st.info(f"📍 선택된 매장: **{selected_store['store_name']}** ({selected_store['team']})")
        
        # 관리자 정보 입력
        admin_id = st.text_input("👤 관리자 ID", key="admin_settings_admin_id")
        admin_pw = st.text_input("🔒 관리자 비밀번호", type="password", key="admin_settings_admin_pw")
        admin_pw_confirm = st.text_input("🔒 비밀번호 확인", type="password", key="admin_settings_admin_pw_confirm")
        
        if admin_pw and admin_pw != admin_pw_confirm:
            st.error("❌ 비밀번호가 일치하지 않습니다.")
            
        if st.button("💾 관리자 등록", key="admin_settings_register_btn"):
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
                st.success(f"✅ {selected_store_name} 관리자 등록이 완료되었습니다!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ 관리자 등록에 실패했습니다.")
                
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

def show_customer_account_setup(sheets_manager):
    """고객 계정 설정"""
    st.markdown("### 👥 고객 계정 등록")
    
    try:
        # 팀 목록 가져오기
        teams = sheets_manager.get_teams()
        
        if not teams:
            st.error("❌ 등록된 팀이 없습니다.")
            return
            
        # 팀 선택
        selected_team = st.selectbox("👥 팀 선택", ["팀을 선택하세요..."] + teams, key="customer_settings_team")
        
        if selected_team == "팀을 선택하세요...":
            return
            
        # 선택된 팀의 매장들 가져오기
        team_stores = sheets_manager.get_stores_by_team(selected_team)
        
        if not team_stores:
            st.warning(f"❗ {selected_team}에 등록된 매장이 없습니다.")
            return
            
        # 매장 선택 (고객 계정이 미등록된 매장만 표시)
        available_stores = [store for store in team_stores if not store.get('user_id', '').strip()]
        
        if not available_stores:
            st.info(f"ℹ️ {selected_team}의 모든 매장에 고객 계정이 이미 등록되어 있습니다.")
            return
            
        store_names = [store['store_name'] for store in available_stores]
        selected_store_name = st.selectbox("🏪 매장 선택", ["매장을 선택하세요..."] + store_names, key="customer_settings_store")
        
        if selected_store_name == "매장을 선택하세요...":
            return
            
        # 선택된 매장 정보 표시
        selected_store = next(store for store in available_stores if store['store_name'] == selected_store_name)
        st.info(f"📍 선택된 매장: **{selected_store['store_name']}** ({selected_store['team']})")
        
        # 고객 계정 정보 입력
        user_id = st.text_input("👤 고객 사용자 ID", key="customer_settings_user_id")
        user_pw = st.text_input("🔒 고객 비밀번호", type="password", key="customer_settings_user_pw")
        user_pw_confirm = st.text_input("🔒 비밀번호 확인", type="password", key="customer_settings_user_pw_confirm")
        
        if user_pw and user_pw != user_pw_confirm:
            st.error("❌ 비밀번호가 일치하지 않습니다.")
            
        if st.button("💾 고객 계정 등록", key="customer_settings_register_btn"):
            if not user_id.strip():
                st.error("❌ 사용자 ID를 입력해주세요.")
                return
                
            if not user_pw.strip():
                st.error("❌ 비밀번호를 입력해주세요.")
                return
                
            if user_pw != user_pw_confirm:
                st.error("❌ 비밀번호가 일치하지 않습니다.")
                return
                
            success = sheets_manager.set_store_customer_account_by_name(selected_store_name, user_id, user_pw)
            if success:
                st.success(f"✅ {selected_store_name} 고객 계정 등록이 완료되었습니다!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ 고객 계정 등록에 실패했습니다.")
                
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")

# 로그아웃 기능 추가
def show_logout_button():
    if 'selected_store_name' in st.session_state:
        if st.button("🚪 로그아웃", key="logout_btn"):
            # 세션 상태 초기화
            if 'selected_store_code' in st.session_state:
                del st.session_state['selected_store_code']
            if 'selected_store_name' in st.session_state:
                del st.session_state['selected_store_name']
            if 'user_level' in st.session_state:
                del st.session_state['user_level']
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
            user_level = st.session_state.get('user_level', 'customer')
            level_text = "관리자" if user_level == 'admin' else "고객"
            st.markdown(f"**🔓 {level_text} 로그인됨:** `{st.session_state['selected_store_name']}`")
            show_logout_button()  # 로그아웃 버튼 추가
            
            # 권한에 따른 메뉴 제한
            if user_level == "admin":
                # 관리자는 모든 메뉴 접근 가능
                tab = st.radio("모드 선택", ["고객 등록", "전산 처리", "계정 등록"])
            else:
                # 고객은 고객 등록만 가능
                tab = st.radio("모드 선택", ["고객 등록"])
                st.info("ℹ️ 고객 모드: 고객 등록만 가능합니다")
        else:
            st.markdown("🔒 로그인되지 않음")
            tab = st.radio("모드 선택", ["로그인", "계정 등록"])

    if tab == "로그인":
        show_login(sheets_manager)
    elif tab == "고객 등록":
        show_customer_view(sheets_manager)
    elif tab == "전산 처리":
        show_admin_view(sheets_manager)
    elif tab == "계정 등록":
        show_store_admin_settings(sheets_manager)

if __name__ == '__main__':
    main()
