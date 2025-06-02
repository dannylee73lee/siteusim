# show_admin_view 함수의 버튼 부분 수정

# 기존 코드를 다음과 같이 변경:

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
                    <div style='flex:3;'>""", unsafe_allow_html=True)

        # 버튼들을 가로로 배열
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # 대기 버튼 - 현재 상태가 대기일 때 활성화
            if customer['status'] == '대기':
                if st.button(f"🟡 대기", key=f"waiting_{customer['id']}", disabled=False):
                    # 대기 상태에서는 처리중으로 변경
                    sheets_manager.update_customer_status(customer['id'], '처리중')
                    st.success(f"ID {customer['id']} → 처리중")
                    st.rerun()
            else:
                st.button(f"⚪ 대기", key=f"waiting_disabled_{customer['id']}", disabled=True)
        
        with col2:
            # 처리중 버튼 - 현재 상태가 처리중일 때 활성화
            if customer['status'] == '처리중':
                st.button(f"🔵 처리중", key=f"processing_{customer['id']}", disabled=True)
            elif customer['status'] == '대기':
                if st.button(f"⚪ 처리중", key=f"processing_inactive_{customer['id']}", disabled=False):
                    # 대기에서 바로 처리중으로 이동 가능
                    sheets_manager.update_customer_status(customer['id'], '처리중')
                    st.success(f"ID {customer['id']} → 처리중")
                    st.rerun()
            else:
                st.button(f"⚪ 처리중", key=f"processing_disabled_{customer['id']}", disabled=True)
        
        with col3:
            # 완료 버튼 - 처리중일 때만 활성화
            if customer['status'] == '처리중':
                if st.button(f"✅ 완료", key=f"complete_{customer['id']}", disabled=False):
                    sheets_manager.update_customer_status(customer['id'], '완료')
                    st.success(f"ID {customer['id']} → 완료")
                    st.rerun()
            else:
                st.button(f"⚪ 완료", key=f"complete_disabled_{customer['id']}", disabled=True)

        st.markdown("""</div></div>""", unsafe_allow_html=True)
