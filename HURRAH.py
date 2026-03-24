import streamlit as st
import pandas as pd

# --- [0. 기본 설정 및 세션 상태 초기화] ---
st.set_page_config(page_title="부경대학교 후라", layout="wide")

if 'menu' not in st.session_state:
    st.session_state.menu = 'home'
if 'stat_type' not in st.session_state:
    st.session_state.stat_type = None

# --- [1. 메인 홈 화면: 4개 세로형 버튼] ---
if st.session_state.menu == 'home':
    st.title("⚾ 부경대학교 후라")
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
        df_p = pd.read_csv("players.csv").sort_values('배번')
        
        # 글자색 지정 함수 (OB: 노란색, YB: 흰색)
        def apply_team_color(x):
            # '팀' 혹은 'OB/YB' 컬럼명에 맞춰 수정 (여기선 '팀' 기준)
            color = 'color: #FFFF00' if x['OB/YB'] == 'OB' else 'color: #FFFFFF'
            return [color] * len(x)

        styled_df = df_p.style.apply(apply_team_color, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
    except Exception as e:
        st.error(f"players.csv 파일을 확인해주세요. (에러: {e})")

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
            df_b = pd.read_csv("batters.csv")
            df_b['타율'] = (df_b['안타'] / df_b['타수']).fillna(0).round(3)
            df_b['선수'] = df_b['배번'].astype(str) + " " + df_b['성명']
            b_cols = ['선수', '타율', '안타', '2루타', '3루타', '홈런', '타점', '득점', '도루']
            st.dataframe(df_b.sort_values('배번')[b_cols], use_container_width=True, hide_index=True,
                         column_config={"타율": st.column_config.NumberColumn(format="%.3f")})
        except: st.error("batters.csv 파일을 확인해주세요.")
            
    elif st.session_state.stat_type == 'pitchers': # 오타 수정 완료
        st.subheader("🥎 투수 공식 기록")
        try:
            df_p = pd.read_csv("pitchers.csv")
            def get_calc_i(i):
                m = int(i); o = round(i-m, 1)
                return m + 0.3333 if o == 0.1 else (m + 0.6666 if o == 0.2 else i)
            df_p['calc_i'] = df_p['이닝'].apply(get_calc_i)
            df_p['평균자책'] = ((df_p['자책점'] * 9) / df_p['calc_i']).replace([float('inf')], 0).fillna(0).round(2)
            df_p['선수'] = df_p['배번'].astype(str) + " " + df_p['성명']
            p_cols = ['선수', '평균자책', '경기', '승', '패', '이닝', '탈삼진', '4사구']
            st.dataframe(df_p.sort_values('배번')[p_cols], use_container_width=True, hide_index=True,
                         column_config={"평균자책": st.column_config.NumberColumn(format="%.2f")})
        except: st.error("pitchers.csv 파일을 확인해주세요.")

# --- [4. 재부리그 순위: 특정 팀 강조 반영] ---
elif st.session_state.menu == 'ranking':
    if st.button("⬅ 메인으로"):
        st.session_state.menu = 'home'
        st.rerun()
        
    st.title("🏆 재부리그 현재 순위")
    
    try:
        df_r = pd.read_csv("ranking.csv")
        
        # 1. 승률 및 데이터 전처리
        df_r['승률'] = (df_r['승'] / (df_r['승'] + df_r['패'])).fillna(0).round(3)
        df_r['팀명'] = df_r['팀명'].astype(str).str.strip() # 공백 제거
        
        # 2. 정렬 (승 -> 승률 -> 최소 실점 우선)
        df_r = df_r.sort_values(
            by=['승', '승률', '실점'], 
            ascending=[False, False, True]
        ).reset_index(drop=True)
        
        # 3. 순위 부여
        df_r.index = df_r.index + 1
        df_r.insert(0, '순위', df_r.index)
        
        # [색상 함수] '부경대 후라' 팀만 노란색으로 강조
        def highlight_team(row):
            # CSV에 적힌 정확한 팀명을 입력해주세요 (예: '부경대 후라' 또는 '허라 베이스볼')
            target_team = "부경대 후라" 
            
            if row['팀명'] == target_team:
                return ['color: #FFD700'] * len(row) # 노란색(Gold) 적용
            return [''] * len(row) # 나머지는 기본색

        # 스타일 적용 (행 전체에 적용)
        styled_df = df_r.style.apply(highlight_team, axis=1)

        # 보여줄 항목 순서
        r_cols = ['순위', '팀명', '승', '패', '무', '승률', '실점', '득점']
        
        st.dataframe(
            styled_df, 
            column_order=r_cols, # 표시 순서 고정
            use_container_width=True, 
            hide_index=True,
            column_config={
                "승률": st.column_config.NumberColumn(format="%.3f")
            }
        )
        
    except FileNotFoundError:
        st.error("ranking.csv 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"오류 발생: {e}")

# --- [5. 재부리그 전적: 일반 굵기 및 색상 최적화] ---
elif st.session_state.menu == 'schedule':
    if st.button("⬅ 메인으로"):
        st.session_state.menu = 'home'
        st.rerun()
        
    st.title("📅 재부리그 전적")
    
    try:
        df_s = pd.read_csv("schedule.csv")
        # 데이터 앞뒤 공백 제거 및 문자열 변환
        df_s['승패'] = df_s['승패'].astype(str).str.strip()
        df_s = df_s.sort_values(by='날짜', ascending=False)

        # [색상 함수] 굵기(Bold) 제거 버전
        def color_win_loss(val):
            if '승' in val:
                return 'color: #FF0000;'  # 빨강 (승리)
            elif '패' in val:
                return 'color: #0000FF;'  # 파랑 (패배)
            elif '무' in val:
                return 'color: #00FF00;'  # 초록 (무승부)
            return 'color: #FFFFFF;'      # 기본 흰색

        # 스타일 적용
        styled_df = df_s.style.applymap(color_win_loss, subset=['승패'])

        st.dataframe(
            styled_df, 
            use_container_width=True, 
            hide_index=True
        )
        
    except FileNotFoundError:
        st.error("schedule.csv 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
