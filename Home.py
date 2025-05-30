import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import pytz
import time
import os
from pathlib import Path
import random

# Google Sheets 연결 설정
@st.cache_resource
def init_google_sheets():
    """Google Sheets 연결 초기화"""
    try:
        # Streamlit Cloud 환경 (secrets 사용)
        if "google_sheets" in st.secrets:
            credentials_dict = st.secrets["google_sheets"]["credentials"]
            sheets_url = st.secrets["google_sheets"]["sheets_url"]
        else:
            # 로컬 환경 (JSON 파일 사용)
            credentials_path = Path("credentials.json")
            if not credentials_path.exists():
                st.error("❌ credentials.json 파일이 없습니다. 설정 가이드를 참고하세요.")
                return None, None
            
            # 환경변수에서 설정 읽기
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
            
            sheets_url = os.getenv("GOOGLE_SHEETS_URL")
            credentials_dict = str(credentials_path)
        
        # Google Sheets 연결
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        if isinstance(credentials_dict, str):
            creds = Credentials.from_service_account_file(credentials_dict, scopes=scope)
        else:
            creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
        
        client = gspread.authorize(creds)
        
        if sheets_url:
            sheet_id = sheets_url.split("/d/")[1].split("/")[0]
            workbook = client.open_by_key(sheet_id)
        else:
            workbook = client.open("유심관리시스템_데이터")
        
        return workbook, client
        
    except Exception as e:
        st.error(f"❌ Google Sheets 연결 오류: {str(e)}")
        return None, None

# CSS 스타일
def load_css():
    return """
    <style>
        .stApp > header {visibility: hidden;}
        .stApp > footer {visibility: hidden;}
        .stApp > div > div > div > div > section > div {padding-top: 1rem;}
        
        .main-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 25px;
            padding: 40px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.15);
            margin: 20px auto;
            max-width: 500px;
            color: white;
        }
        
        .store-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .store-name {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .store-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .status-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
        }
        
        .ticket-result {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 40px;
            border-radius: 25px;
            text-align: center;
            margin: 30px 0;
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.3);
        }
        
        .ticket-number {
            font-size: 4rem;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 15px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
    </style>
    """

# 개인정보 마스킹 함수들
def mask_phone(phone, is_admin_view=False):
    """전화번호 마스킹"""
    if is_admin_view:
        return phone
    else:
        numbers = ''.join(filter(str.isdigit, phone))
        if len(numbers) == 11:
            return f"{numbers[:3]}-****-{numbers[7:]}"
        return phone

def mask_name(name):
    """이름 마스킹"""
    if len(name) <= 1:
        return name
    elif len(name) == 2:
        return name[0] + '*'
    elif len(name) == 3:
        return name[0] + '*' + name[2]
    elif len(name) == 4:
        return name[0] + '**' + name[3]
    else:
        return name[0] + '*' * (len(name) - 2) + name[-1]

def format_korean_datetime(dt=None):
    """한국 시간 형식으로 변환"""
    if dt is None:
        korea_tz = pytz.timezone('Asia/Seoul')
        dt = datetime.now(korea_tz)
    elif dt.tzinfo is None:
        korea_tz = pytz.timezone('Asia/Seoul')
        dt = korea_tz.localize(dt)
    
    return dt.strftime("%y-%m-%d, %I:%M %p")

def format_phone_number(phone):
    """전화번호 형식화"""
    numbers = ''.join(filter(str.isdigit, phone))
    if len(numbers) == 11:
        return f"{numbers[:3]}-{numbers[3:7]}-{numbers[7:]}"
    return phone

def is_phone_duplicate(stored_phone, input_phone):
    """전화번호 중복 확인"""
    numbers_only = ''.join(filter(str.isdigit, input_phone))
    if len(numbers_only) == 11:
        formatted_input = f"{numbers_only[:3]}-{numbers_only[3:7]}-{numbers_only[7:]}"
    else:
        formatted_input = input_phone
    
    return stored_phone == formatted_input

# Google Sheets 데이터 관리 클래스
class SheetsManager:
    def __init__(self, workbook):
        self.workbook = workbook
        
    def get_all_stores(self):
        """모든 매장 정보 조회"""
        try:
            sheet = self.workbook.worksheet("stores")
            all_values = sheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                return []
            
            headers = all_values[0]
            data = []
            
            for row in all_values[1:]:
                if not any(cell.strip() for cell in row if cell):
                    continue
                
                while len(row) < len(headers):
                    row.append('')
                
                row_dict = {}
                for i, header in enumerate(headers):
                    if i < len(row):
                        row_dict[header] = row[i]
                    else:
                        row_dict[header] = ''
                
                if row_dict.get('store_code') and row_dict.get('store_name'):
                    data.append(row_dict)
            
            return data
            
        except gspread.exceptions.WorksheetNotFound:
            return []
        except Exception as e:
            st.error(f"매장 정보 조회 오류: {str(e)}")
            return []
    
    def get_store_by_code(self, store_code):
        """특정 매장 정보 조회"""
        stores = self.get_all_stores()
        for store in stores:
            if store.get('store_code') == store_code:
                return store
        return None
    
    def get_customers(self, store_code=None):
        """고객 목록 조회"""
        try:
            sheet = self.workbook.worksheet("customers")
            all_values = sheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                return []
            
            headers = all_values[0]
            data = []
            
            for i, row in enumerate(all_values[1:], start=2):
                try:
                    if not any(cell.strip() for cell in row if cell):
                        continue
                    
                    while len(row) < len(headers):
                        row.append('')
                    
                    row_dict = {}
                    for j, header in enumerate(headers):
                        if j < len(row):
                            row_dict[header] = row[j]
                        else:
                            row_dict[header] = ''
                    
                    if not row_dict.get('id') or not row_dict.get('name'):
                        continue
                    
                    try:
                        row_dict['id'] = int(row_dict['id']) if row_dict['id'].isdigit() else 0
                    except (ValueError, AttributeError):
                        row_dict['id'] = 0
                    
                    # store_ticket_number 처리
                    if row_dict.get('store_ticket_number'):
                        try:
                            row_dict['store_ticket_number'] = int(row_dict['store_ticket_number'])
                        except (ValueError, TypeError):
                            row_dict['store_ticket_number'] = 0
                    else:
                        row_dict['store_ticket_number'] = 0
                    
                    if not row_dict.get('status'):
                        row_dict['status'] = '대기'
                    if not row_dict.get('store_code'):
                        row_dict['store_code'] = 'UNKNOWN'
                    if not row_dict.get('service_type'):
                        row_dict['service_type'] = '기타'
                    
                    data.append(row_dict)
                    
                except Exception as e:
                    continue
            
            if store_code:
                data = [row for row in data if row.get('store_code') == store_code]
            
            # datetime 변환
            for row in data:
                if row.get('registered_time'):
                    try:
                        time_str = row['registered_time']
                        row['registered_time'] = datetime.strptime(time_str, "%y-%m-%d, %I:%M %p")
                    except:
                        try:
                            if 'T' in time_str:
                                row['registered_time'] = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                            else:
                                row['registered_time'] = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                        except:
                            row['registered_time'] = datetime.now()
                else:
                    row['registered_time'] = datetime.now()
            
            return data
            
        except gspread.exceptions.WorksheetNotFound:
            return []
        except Exception as e:
            return []
    
    def add_customer(self, name, phone, service_type, store_code):
        """새 고객 추가 - 매장별 티켓 번호 관리"""
        try:
            sheet = self.workbook.worksheet("customers")
            all_values = sheet.get_all_values()
            
            # 헤더가 없으면 추가
            if not all_values:
                headers = ["id", "name", "phone", "service_type", "registered_time", "status", "store_code", "estimated_time", "store_ticket_number"]
                sheet.append_row(headers)
                all_values = [headers]
            
            # 헤더에 store_ticket_number 컬럼이 없으면 추가
            headers = all_values[0]
            if "store_ticket_number" not in headers:
                headers.append("store_ticket_number")
                sheet.update('A1:I1', [headers])
            
            # 전체 ID와 매장별 티켓 번호 계산
            new_id = 1
            store_ticket_number = 1
            
            if len(all_values) > 1:
                try:
                    existing_ids = []
                    store_ticket_numbers = []
                    
                    for row in all_values[1:]:
                        if row and len(row) > 0:
                            # 전체 ID 수집
                            if row[0]:
                                try:
                                    existing_ids.append(int(row[0]))
                                except (ValueError, IndexError):
                                    continue
                            
                            # 같은 매장의 티켓 번호 수집
                            if len(row) > 6 and row[6] == store_code:
                                # store_ticket_number가 있는 경우
                                if len(row) > 8 and row[8]:
                                    try:
                                        store_ticket_numbers.append(int(row[8]))
                                    except (ValueError, IndexError):
                                        continue
                    
                    # 새 전체 ID 생성
                    if existing_ids:
                        new_id = max(existing_ids) + 1
                    else:
                        new_id = 1
                    
                    # 새 매장별 티켓 번호 생성
                    if store_ticket_numbers:
                        store_ticket_number = max(store_ticket_numbers) + 1
                    else:
                        store_ticket_number = 1
                        
                except Exception as e:
                    new_id = len(all_values)
                    store_ticket_number = 1
            
            # 예상 시간 계산
            estimated_time = 3 if service_type in ["유심교체", "유심재설정"] else 10
            current_time = format_korean_datetime()
            
            # 새 행 데이터 준비
            new_row = [
                str(new_id),
                str(name),
                str(phone),
                str(service_type),
                current_time,
                "대기",
                str(store_code),
                str(estimated_time),
                str(store_ticket_number)
            ]
            
            # 행 추가
            sheet.append_row(new_row)
            return store_ticket_number
            
        except gspread.exceptions.WorksheetNotFound:
            try:
                customers_sheet = self.workbook.add_worksheet(title="customers", rows="1000", cols="10")
                headers = ["id", "name", "phone", "service_type", "registered_time", "status", "store_code", "estimated_time", "store_ticket_number"]
                customers_sheet.append_row(headers)
                return self.add_customer(name, phone, service_type, store_code)
            except Exception as create_error:
                return None
                
        except Exception as e:
            return None
    
    def get_settings(self):
        """설정 조회"""
        try:
            sheet = self.workbook.worksheet("settings")
            all_values = sheet.get_all_values()
            
            if not all_values or len(all_values) < 2:
                return {
                    'usim_change_time': 3,
                    'usim_reset_time': 3,
                    'other_service_time': 10
                }
            
            settings = {}
            for row in all_values[1:]:
                if len(row) >= 2 and row[0] and row[1]:
                    try:
                        if row[1].isdigit():
                            settings[row[0]] = int(row[1])
                        else:
                            settings[row[0]] = row[1]
                    except:
                        settings[row[0]] = row[1]
            
            default_settings = {
                'usim_change_time': 3,
                'usim_reset_time': 3,
                'other_service_time': 10
            }
            
            for key, default_value in default_settings.items():
                if key not in settings:
                    settings[key] = default_value
            
            return settings
            
        except gspread.exceptions.WorksheetNotFound:
            return {
                'usim_change_time': 3,
                'usim_reset_time': 3,
                'other_service_time': 10
            }
        except Exception as e:
            return {
                'usim_change_time': 3,
                'usim_reset_time': 3,
                'other_service_time': 10
            }

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

    def update_customer_status(self, customer_id, new_status):
        """고객 상태 업데이트"""
        try:
            sheet = self.workbook.worksheet("customers")
            all_values = sheet.get_all_values()
            headers = all_values[0]
            for i, row in enumerate(all_values[1:], start=2):
                if row[0] == str(customer_id):
                    sheet.update_cell(i, headers.index('status') + 1, new_status)
                    break
        except Exception as e:
            st.error(f"상태 업데이트 오류: {str(e)}")

    def get_store_ticket_numbers(self, store_code):
        """특정 매장의 티켓 번호 목록 조회"""
        try:
            customers = self.get_customers(store_code)
            ticket_numbers = []
            
            for customer in customers:
                if customer.get('store_ticket_number'):
                    try:
                        ticket_numbers.append(int(customer['store_ticket_number']))
                    except (ValueError, TypeError):
                        continue
            
            return sorted(ticket_numbers)
        except Exception as e:
            return []

    def get_next_store_ticket_number(self, store_code):
        """특정 매장의 다음 티켓 번호 미리보기"""
        try:
            ticket_numbers = self.get_store_ticket_numbers(store_code)
            if ticket_numbers:
                return max(ticket_numbers) + 1
            else:
                return 1
        except Exception:
            return 1

# 헬퍼 함수들
def get_store_name(store_code, sheets_manager):
    """매장 코드로 매장명 가져오기"""
    store_info = sheets_manager.get_store_by_code(store_code)
    if store_info:
        return store_info['store_name']
    
    # 기본 매장 맵
    store_map = {
        'STORE001': '강남점',
        'STORE002': '홍대점', 
        'STORE003': '신촌점'
    }
    return store_map.get(store_code, '테스트점')

def get_current_status(store_code, sheets_manager):
    """현재 대기 현황 가져오기"""
    try:
        customers = sheets_manager.get_customers(store_code)
        waiting_customers = [c for c in customers if c['status'] == '대기']
        waiting_count = len(waiting_customers)
        
        # 대기 중인 고객들의 예상 시간 합계
        total_estimated_time = 0
        for customer in waiting_customers:
            estimated_time = int(customer.get('estimated_time', 5))
            total_estimated_time += estimated_time
        
        # 기본 대기시간 추가
        total_estimated_time += random.randint(0, 5)
        
        return waiting_count, total_estimated_time
    except Exception as e:
        # 오류 시 기본값 반환
        waiting = random.randint(1, 5)
        time_estimate = waiting * 5 + random.randint(2, 8)
        return waiting, time_estimate

def validate_input(phone, name):
    """입력 검증"""
    if not phone or not name:
        return False, "모든 필드를 입력해주세요."
    
    numbers = ''.join(filter(str.isdigit, phone))
    if len(numbers) < 10 or len(numbers) > 11:
        return False, "올바른 전화번호를 입력해주세요. (10-11자리)"
    
    if not numbers.startswith(('010', '011', '016', '017', '018', '019')):
        return False, "유효하지 않은 전화번호입니다."
    
    name = name.strip()
    if len(name) < 2 or len(name) > 10:
        return False, "이름은 2-10자 사이로 입력해주세요."
    
    return True, "검증 성공"

def register_customer(phone, name, store_code, service_type, sheets_manager):
    """고객 등록"""
    try:
        formatted_phone = format_phone_number(phone)
        masked_name = mask_name(name)
        stored_phone = formatted_phone
        
        # 중복 확인
        existing_customers = sheets_manager.get_customers(store_code)
        
        for customer in existing_customers:
            if is_phone_duplicate(customer['phone'], formatted_phone):
                return None, "이미 등록된 전화번호입니다."
        
        # 고객 추가
        store_ticket_number = sheets_manager.add_customer(masked_name, stored_phone, service_type, store_code)
        
        if store_ticket_number:
            return store_ticket_number, "등록 성공"
        else:
            return None, "등록 중 오류가 발생했습니다."
        
    except Exception as e:
        return None, f"등록 중 오류가 발생했습니다: {str(e)}"

# 고객 입력 화면
def show_input_screen(store_name, store_code):
    """고객 입력 화면"""
    
    # CSS 로드
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # 세션 상태 초기화
    if 'show_ticket' not in st.session_state:
        st.session_state.show_ticket = False
    if 'ticket_number' not in st.session_state:
        st.session_state.ticket_number = None
    if 'ticket_time' not in st.session_state:
        st.session_state.ticket_time = None
    
    # SheetsManager 인스턴스 가져오기
    workbook, client = init_google_sheets()
    if workbook is None:
        st.error("🔧 Google Sheets 설정이 필요합니다.")
        return
    
    sheets_manager = SheetsManager(workbook)
    
    if st.session_state.show_ticket:
        show_ticket_screen()
    else:
        show_customer_input_form(store_name, store_code, sheets_manager)

def show_customer_input_form(store_name, store_code, sheets_manager):
    """고객 정보 입력 폼"""
    
    # 현재 대기 현황
    waiting_count, estimated_time = get_current_status(store_code, sheets_manager)
    
    # 다음 티켓 번호 미리보기
    next_ticket = sheets_manager.get_next_store_ticket_number(store_code)
    
    # 메인 헤더
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 25px; padding: 30px; text-align: center; color: white; margin: 20px 0;">
        <h1 style="color: white; margin: 10px 0; font-size: 2.5rem;">📱 {store_name}</h1>
        <p style="color: white; opacity: 0.9; margin: 10px 0; font-size: 1.1rem;">유심 교체 서비스</p>
        <div style="background: rgba(255,255,255,0.2); border-radius: 15px; padding: 15px; margin-top: 20px;">
            <p style="color: white; margin: 0; font-size: 1.1rem;">다음 발급 번호: <strong>{next_ticket}번</strong></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 현황 정보
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.05); border-radius: 15px; margin: 5px;">
            <p style="margin: 5px 0; font-size: 1.1rem; color: #666;">현재 대기</p>
            <p style="margin: 5px 0; font-size: 2.2rem; font-weight: bold; color: #667eea;">{waiting_count}명</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.05); border-radius: 15px; margin: 5px;">
            <p style="margin: 5px 0; font-size: 1.1rem; color: #666;">예상 시간</p>
            <p style="margin: 5px 0; font-size: 2.2rem; font-weight: bold; color: #667eea;">약 {estimated_time}분</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 입력 폼 헤더
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 25px; padding: 30px; margin: 20px 0; text-align: center;">
        <h3 style="color: white; margin: 0;">✍️ 간단 정보 입력</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 자동 새로고침 버튼
    if st.button("🔄 현황 새로고침", use_container_width=True):
        st.rerun()
    
    # 설정 정보 가져오기
    settings = sheets_manager.get_settings()
    
    # 세션 상태에 폼 초기화 플래그 추가
    if 'form_reset' not in st.session_state:
        st.session_state.form_reset = False
    
    with st.form("customer_registration", clear_on_submit=st.session_state.form_reset):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            phone = st.text_input(
                "📱 전화번호",
                placeholder="01012345678",
                help="숫자만 입력하세요 (하이픈 없이)",
                value="" if st.session_state.form_reset else st.session_state.get("phone_value", "")
            )
        
        with col2:
            name = st.text_input(
                "👤 이름", 
                placeholder="홍길동",
                help="실명을 입력해주세요",
                value="" if st.session_state.form_reset else st.session_state.get("name_value", "")
            )
        
        # 서비스 유형 선택
        service_options = [
            f"유심교체 ({settings.get('usim_change_time', 3)}분)",
            f"유심재설정 ({settings.get('usim_reset_time', 3)}분)",
            f"기타 ({settings.get('other_service_time', 10)}분)"
        ]
        service_type = st.selectbox(
            "방문 목적", 
            service_options,
            index=0 if st.session_state.form_reset else st.session_state.get("service_index", 0)
        )
        service_name = service_type.split(' (')[0]  # "유심교체 (3분)" -> "유심교체"
        
        # 실시간 미리보기
        preview_container = st.container()
        
        # 등록 버튼
        submitted = st.form_submit_button(
            "🎫 대기번호 받기",
            use_container_width=True
        )
        
        # 미리보기 표시
        with preview_container:
            if phone:
                formatted_phone = format_phone_number(phone)
                masked_phone = mask_phone(formatted_phone, is_admin_view=False)
                st.caption(f"📱 형식: {formatted_phone}")
                st.caption(f"🔒 표시: {masked_phone}")
            
            if name:
                masked_name = mask_name(name)
                st.caption(f"🔒 저장될 이름: {masked_name}")
        
        if submitted:
            # 입력값을 세션 상태에 임시 저장
            st.session_state.phone_value = phone
            st.session_state.name_value = name
            st.session_state.service_index = service_options.index(service_type)
            
            is_valid, message = validate_input(phone, name)
            
            if is_valid:
                with st.spinner("등록 중..."):
                    store_ticket_number, result_message = register_customer(phone, name, store_code, service_name, sheets_manager)
                    
                    if store_ticket_number:
                        st.success(f"✅ 등록 완료! 매장 티켓 번호: {store_ticket_number}번")
                        
                        # 폼 초기화 플래그 설정
                        st.session_state.form_reset = True
                        st.session_state.phone_value = ""
                        st.session_state.name_value = ""
                        st.session_state.service_index = 0
                        
                        st.session_state.ticket_number = store_ticket_number
                        st.session_state.show_ticket = True
                        st.session_state.ticket_time = time.time()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error(f"❌ {result_message}")
            else:
                st.error(f"❌ {message}")
        
        # 폼 초기화 플래그 리셋
        if st.session_state.form_reset:
            st.session_state.form_reset = False
    
    # 빠른 팁
    st.markdown("""
    <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); border-radius: 20px; padding: 25px; margin: 20px 0; color: white;">
        <h3 style="color: white; margin: 0 0 15px 0; font-size: 1.3rem;">💡 이용 안내</h3>
        <div style="line-height: 1.8; font-size: 1rem;">
            • 전화번호는 숫자만 입력하세요<br>
            • 대기번호 발급 후 호출시까지 대기해주세요<br>
            • 예상시간은 실시간으로 변동될 수 있습니다<br>
            • 고객님의 개인정보는 필요한 목적에만 사용되며, 알아볼 수 없도록 처리한 뒤 안전하게 보관·삭제됩니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_ticket_screen():
    """대기번호 발급 화면"""
    
    st.markdown(f"""
    <div class="ticket-result">
        <div style="font-size: 3rem; margin-bottom: 20px;">🎉</div>
        <div class="ticket-number">{st.session_state.ticket_number}번</div>
        <div style="font-size: 1.3rem; line-height: 1.8;">
            <strong>대기번호가 발급되었습니다!</strong><br>
            호출시 창구로 와주세요<br><br>
            📞 휴대폰과 신분증을 준비해주세요
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 즉시 초기화 버튼
    if st.button("🏠 처음으로 돌아가기"):
        st.session_state.show_ticket = False
        st.session_state.ticket_number = None
        st.session_state.ticket_time = None
        st.rerun()
    
    # 자동 복귀 카운트다운 표시
    if st.session_state.ticket_time:
        elapsed = time.time() - st.session_state.ticket_time
        remaining = max(0, 5 - int(elapsed))
        
        if remaining > 0:
            st.info(f"⏰ {remaining}초 후 자동으로 처음 화면으로 돌아갑니다...")
            time.sleep(1)
            st.rerun()
        else:
            # 5초가 지나면 자동으로 초기화
            st.session_state.show_ticket = False
            st.session_state.ticket_number = None
            st.session_state.ticket_time = None
            st.rerun()

# 메인 함수
def main():
    """메인 함수"""
    st.set_page_config(
        page_title="유심 교체 서비스",
        page_icon="📱",
        layout="centered"
    )
    
    # 매장 정보 설정
    store_code = st.query_params.get("store", "STORE001")
    
    # Google Sheets 연결
    workbook, client = init_google_sheets()
    if workbook is None:
        st.error("🔧 Google Sheets 설정이 필요합니다.")
        st.stop()
    
    sheets_manager = SheetsManager(workbook)
    store_name = get_store_name(store_code, sheets_manager)
    
    # 고객 입력 화면 표시
    show_input_screen(store_name, store_code)

# 추가 유틸리티 함수들
def get_store_waiting_summary(sheets_manager):
    """모든 매장의 대기 현황 요약"""
    try:
        all_stores = sheets_manager.get_all_stores()
        summary = []
        
        for store in all_stores:
            store_code = store['store_code']
            store_name = store['store_name']
            waiting_count, estimated_time = get_current_status(store_code, sheets_manager)
            next_ticket = sheets_manager.get_next_store_ticket_number(store_code)
            
            summary.append({
                'store_code': store_code,
                'store_name': store_name,
                'waiting_count': waiting_count,
                'estimated_time': estimated_time,
                'next_ticket': next_ticket
            })
        
        return summary
    except Exception as e:
        return []

def get_store_ticket_history(store_code, sheets_manager, days=7):
    """특정 매장의 최근 티켓 발급 이력"""
    try:
        customers = sheets_manager.get_customers(store_code)
        
        # 최근 N일간 데이터 필터링
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_customers = [
            c for c in customers 
            if c.get('registered_time') and c['registered_time'] >= cutoff_date
        ]
        
        # 날짜별 발급 수 집계
        daily_counts = {}
        for customer in recent_customers:
            date_key = customer['registered_time'].strftime('%Y-%m-%d')
            if date_key not in daily_counts:
                daily_counts[date_key] = 0
            daily_counts[date_key] += 1
        
        return daily_counts
    except Exception as e:
        return {}

if __name__ == "__main__":
    main()
