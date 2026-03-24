import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="재부리그 야구단", page_icon="⚾", layout="centered")

# 2. 어떤 화면을 보여줄지 결정하는 '상태' 초기화
if 'menu' not in st.session_state:
    st.session_state.menu = 'home'

# --- 함수: 홈 화면으로 돌아가기 ---
def go_home():
    st.session_state.menu = 'home'

# --- [메인 화면: 버튼 3개만 보임] ---
if st.session_state.menu == 'home':
# 'index'를 'html'로만 바꾸면 됩니다!
    st.markdown("<h1 style='text-align: center;'>⚾ 재부리그 야구단</h1>", unsafe_allow_html=True)
    st.write("") # 간격 조절
    st.write("")

    # 큰 버튼 3개를 세로로 배치 (폭을 꽉 채워서 클릭하기 편하게!)
    if st.button("📋 선수단 배번 확인", use_container_width=True):
        st.session_state.menu = 'roster'
        st.rerun()

    if st.button("📈 선수단 세부 기록", use_container_width=True):
        st.session_state.menu = 'stats'
        st.rerun()

    if st.button("🏆 재부리그 팀 기록", use_container_width=True):
        st.session_state.menu = 'league'
        st.rerun()

# --- [1번 메뉴: 선수단 배번] ---
elif st.session_state.menu == 'roster':
    if st.button("⬅ 뒤로가기"): go_home()
    st.title("📋 선수단 배번 명단")

    # 파일 읽어오기 (이게 끝입니다!)
    try:
        df = pd.read_csv("players.csv")
        df = df.sort_values(by="배번")
    except:
        st.error("players.csv 파일을 찾을 수 없어요. 파일을 먼저 만들어주세요!")
    
    # 2. 색상을 입히는 함수 정의
    def highlight_ob_yb(row):
        # OB는 노란색, YB는 하얀색 글자로 설정
        if row['OB/YB'] == 'OB':
            return ['color: yellow'] * len(row) # 노란색 글자
        elif row['OB/YB'] == 'YB':
            return ['color: white'] * len(row) # 하얀색 글자
        return [''] * len(row)

    # 3. 스타이 적용해서 출력
    st.write("💡 노란색은 **OB**, 흰색은 **YB** 선수입니다.")
    
    # .style.apply를 사용하면 조건에 맞게 색이 칠해진 표가 나옵니다.
    st.dataframe(
        df.style.apply(highlight_ob_yb, axis=1), 
        use_container_width=True, 
        hide_index=True
    )

# --- [2번 메뉴: 선수단 기록] ---
elif st.session_state.menu == 'stats':
    if st.button("⬅ 뒤로가기"): go_home()
    st.title("📈 선수단 기록")
    st.info("시즌 누적 기록입니다.")
    # 임시 표
    st.write("안타, 홈런 등 상세 지표가 여기에 나타납니다.")

# --- [3번 메뉴: 재부리그 팀 기록] ---
elif st.session_state.menu == 'league':
    if st.button("⬅ 뒤로가기"): go_home()
    st.title("🏆 재부리그 팀 기록")
    st.success("최근 경기: 우리팀 5 vs 2 상대팀 (승)")
    st.write("리그 전체 순위와 경기 일정을 확인하세요.")