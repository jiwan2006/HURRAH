import streamlit as st
import pandas as pd

# --- [0. 기본 설정 및 세션 상태 초기화] ---
st.set_page_config(page_title="HURRAH", layout="wide")

삼성 브라우저와 모바일 환경에서 버전이나 다크 모드 설정에 상관없이 모든 표와 버튼이 선명하게 보이도록 최적화한 최종 통합 코드입니다.

기존의 모든 디자인 로직(노란색 강조, 승패 색상)은 유지하면서, 어떤 기기에서도 배경이 하얗게 뜨지 않도록 강력한 스타일 시트를 적용했습니다.

⚾ 부경대 후라(HURRAH) 최종 최적화 코드
Python
import streamlit as st
import pandas as pd

# --- [0. 기본 설정 및 모바일 최적화 스타일] ---
st.set_page_config(page_title="부경대학교 후라", layout="wide")

# 모든 환경(특히 삼성 인터넷)에서 다크 테마를 강제하고 버튼/표 시인성을 높이는 CSS
st.markdown("""
    <style>
    /* 전체 배경 및 기본 글자색 고정 */
    .stApp {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }
    
    /* 메인 화면 및 모든 버튼 스타일 강화 */
    div.stButton > button {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 2px solid #FFD700 !important; /* 노란색 테두리 */
        border-radius: 8px !important;
        padding: 0.6em 1em !important;
        font-weight: bold !important;
        width: 100% !important;
        margin-bottom: 5px !important;
    }

    /* 버튼에 마우스 올리거나 눌렀을 때 */
    div.stButton > button:hover, div.stButton > button:active {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }

    /* 표(DataFrame) 배경 및 테두리 설정 */
    div[data-testid="stDataFrame"], .stTable {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 5px !important;
    }

    /* 뒤로가기 버튼 등 작은 버튼 색상 별도 지정 (선택사항) */
    button[kind="secondary"] {
        border: 1px solid #555 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 구글 스프레드시트 CSV 링크 설정
URL_PLAYERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0AIsQ8X9XoO2hs0gW40WgtSF22eXNEkKGbNw2rFeMJ6Y8q16a45w3Pg1n8uV_RHnccvBbn9q4yfAR/pub?gid=0&single=true&output=csv"
URL_BATTERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0AIsQ8X9XoO2hs0gW40WgtSF22eXNEkKGbNw2rFeMJ6Y8q16a45w3Pg1n8uV_RHnccvBbn9q4yfAR/pub?gid=214942261&single=true&output=csv"
URL_PITCHERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0AIsQ8X9XoO2hs0gW40WgtSF22eXNEkKGbNw2rFeMJ6Y8q16a45w3Pg1n8uV_RHnccvBbn9q4yfAR/pub?gid=59278675&single=true&output=csv"
URL_RANKING = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0AIsQ8X9XoO2hs0gW40WgtSF22eXNEkKGbNw2rFeMJ6Y8q16a45w3Pg1n8uV_RHnccvBbn9q4yfAR/pub?gid=2059541834&single=true&output=csv"
URL_SCHEDULE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0AIsQ8X9XoO2hs0gW40WgtSF22eXNEkKGbNw2rFeMJ6Y8q16a45w3Pg1n8uV_RHnccvBbn9q4yfAR/pub?gid=2067842394&single=true&output=csv"

# 데이터 로드 함수 (캐시 적용: 5분마다 자동 갱신)
@st.cache_data(ttl=60)
def load_data(url):
    return pd.read_csv(url)

if 'menu' not in st.session_state:
    st.session_state.menu = 'home'
if 'stat_type' not in st.session_state:
    st.session_state.stat_type = None

# --- [1. 메인 홈 화면: 4개 세로형 버튼] ---
if st.session_state.menu == 'home':
    st.title("⚾ HURRAH")
    st.divider()
    
    if st.button("\n🔢 선수단 배번\n", use_container_width=True):
        st.session_state.menu = 'roster'
        st.rerun()
    if st.button("\n📊 선수단 기록\n", use_container_width=True):
        st.session_state.menu = 'stats'
        st.rerun()
    if st.button("\n🏆 재부리그 순위\n", use_container_width=True):
        st.session_state.menu = 'ranking'
        st.rerun()
    if st.button("\n📅 재부리그 전적\n", use_container_width=True):
        st.session_state.menu = 'schedule'
        st.rerun()

# --- [2. 선수단 배번: 사진과 동일한 노란색/흰색 스타일] ---
elif st.session_state.menu == 'roster':
    if st.button("⬅ 뒤로가기"):
        st.session_state.menu = 'home'
        st.rerun()
    
    st.title("📋 선수단 배번 명단")
    st.markdown("💡 노란색은 OB, 흰색은 YB 선수입니다.")
    
    try:
        df_p = load_data(URL_PLAYERS).sort_values('배번')
        
        def apply_team_color(x):
            color = 'color: #FFFF00' if x['OB/YB'] == 'OB' else 'color: #FFFFFF'
            return [color] * len(x)

        styled_df = df_p.style.apply(apply_team_color, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"데이터를 불러올 수 없습니다. (에러: {e})")

# --- [3. 선수단 기록: 타자/투수 전체 기록 표] ---
elif st.session_state.menu == 'stats':
    if st.button("⬅ 메인으로"):
        st.session_state.menu = 'home'
        st.session_state.stat_type = None
        st.rerun()
    st.title("📊 선수단 상세 기록")
    
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        if st.button("🏃 타자 기록 전체", use_container_width=True):
            st.session_state.stat_type = 'batters'
    with col_stat2:
        if st.button("🥎 투수 기록 전체", use_container_width=True):
            st.session_state.stat_type = 'pitchers'

    st.divider()

    if st.session_state.stat_type == 'batters':
        st.subheader("🏃 타자 공식 기록")
        try:
            df_b = load_data(URL_BATTERS)
            df_b['타율'] = (df_b['안타'] / df_b['타수']).fillna(0).round(3)
            df_b['선수'] = df_b['배번'].astype(str) + " " + df_b['성명']
            b_cols = ['선수', '타율', '안타', '2루타', '3루타', '홈런', '타점', '득점', '도루']
            st.dataframe(df_b.sort_values('배번')[b_cols], use_container_width=True, hide_index=True,
                         column_config={"타율": st.column_config.NumberColumn(format="%.3f")})
        except: st.error("타자 기록 데이터를 확인해주세요.")
            
    elif st.session_state.stat_type == 'pitchers':
        st.subheader("🥎 투수 공식 기록")
        try:
            df_p = load_data(URL_PITCHERS)
            def get_calc_i(i):
                m = int(i); o = round(i-m, 1)
                return m + 0.3333 if o == 0.1 else (m + 0.6666 if o == 0.2 else i)
            df_p['calc_i'] = df_p['이닝'].apply(get_calc_i)
            df_p['평균자책'] = ((df_p['자책점'] * 9) / df_p['calc_i']).replace([float('inf')], 0).fillna(0).round(2)
            df_p['선수'] = df_p['배번'].astype(str) + " " + df_p['성명']
            p_cols = ['선수', '평균자책', '경기', '승', '패', '이닝', '탈삼진', '4사구']
            st.dataframe(df_p.sort_values('배번')[p_cols], use_container_width=True, hide_index=True,
                         column_config={"평균자책": st.column_config.NumberColumn(format="%.2f")})
        except: st.error("투수 기록 데이터를 확인해주세요.")

# --- [4. 재부리그 순위: 특정 팀 강조 반영] ---
elif st.session_state.menu == 'ranking':
    if st.button("⬅ 메인으로"):
        st.session_state.menu = 'home'
        st.rerun()
        
    st.title("🏆 재부리그 현재 순위")
    
    try:
        df_r = load_data(URL_RANKING)
        df_r['승률'] = (df_r['승'] / (df_r['승'] + df_r['패'])).fillna(0).round(3)
        df_r['팀명'] = df_r['팀명'].astype(str).str.strip()
        
        df_r = df_r.sort_values(by=['승', '승률', '실점'], ascending=[False, False, True]).reset_index(drop=True)
        df_r.index = df_r.index + 1
        df_r.insert(0, '순위', df_r.index)
        
        def highlight_team(row):
            target_team = "부경대 후라" 
            if row['팀명'] == target_team:
                return ['color: #FFD700'] * len(row)
            return [''] * len(row)

        styled_df = df_r.style.apply(highlight_team, axis=1)
        r_cols = ['순위', '팀명', '승', '패', '무', '승률', '실점', '득점']
        
        st.dataframe(styled_df, column_order=r_cols, use_container_width=True, hide_index=True,
                     column_config={"승률": st.column_config.NumberColumn(format="%.3f")})
        
    except Exception as e:
        st.error(f"순위 데이터를 불러오는 중 오류 발생: {e}")

# --- [5. 재부리그 전적: 일반 굵기 및 색상 최적화] ---
elif st.session_state.menu == 'schedule':
    if st.button("⬅ 메인으로"):
        st.session_state.menu = 'home'
        st.rerun()
        
    st.title("📅 재부리그 전적")
    
    try:
        df_s = load_data(URL_SCHEDULE)
        df_s['승패'] = df_s['승패'].astype(str).str.strip()
        df_s = df_s.sort_values(by='날짜', ascending=False)

        def color_win_loss(val):
            if '승' in val: return 'color: #FF0000;'
            elif '패' in val: return 'color: #0000FF;'
            elif '무' in val: return 'color: #00FF00;'
            return 'color: #FFFFFF;'

        styled_df = df_s.style.applymap(color_win_loss, subset=['승패'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"전적 데이터를 불러오는 중 오류 발생: {e}")
