import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import DatabaseManager
from typing import Dict, Any

# ページ設定
st.set_page_config(
    page_title="家計簿アプリ",
    page_icon="💰",
    layout="wide"
)

# データベースマネージャーの初期化
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# サイドバー
st.sidebar.title("💰 家計簿アプリ")
page = st.sidebar.selectbox(
    "ページを選択",
    ["📊 ダッシュボード", "➕ 収支記録", "📋 取引履歴", "📈 分析"]
)

# メインコンテンツ
if page == "📊 ダッシュボード":
    st.title("📊 ダッシュボード")
    
    # 期間選択
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox(
            "期間を選択",
            ["今月", "先月", "過去3ヶ月", "過去6ヶ月", "今年", "カスタム"]
        )
    
    # 期間の計算
    today = datetime.now()
    if period == "今月":
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif period == "先月":
        last_month = today.replace(day=1) - timedelta(days=1)
        start_date = last_month.replace(day=1).strftime("%Y-%m-%d")
        end_date = last_month.strftime("%Y-%m-%d")
    elif period == "過去3ヶ月":
        start_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif period == "過去6ヶ月":
        start_date = (today - timedelta(days=180)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif period == "今年":
        start_date = today.replace(month=1, day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    else:  # カスタム
        with col2:
            start_date = st.date_input("開始日", value=today - timedelta(days=30)).strftime("%Y-%m-%d")
            end_date = st.date_input("終了日", value=today).strftime("%Y-%m-%d")
    
    # サマリー情報の取得
    summary = db.get_summary(start_date, end_date)
    
    # メトリクス表示
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="総収入",
            value=f"¥{summary['total_income']:,.0f}",
            delta=f"{summary['income_count']}件"
        )
    
    with col2:
        st.metric(
            label="総支出",
            value=f"¥{summary['total_expense']:,.0f}",
            delta=f"{summary['expense_count']}件"
        )
    
    with col3:
        balance_color = "normal" if summary['balance'] >= 0 else "inverse"
        st.metric(
            label="収支バランス",
            value=f"¥{summary['balance']:,.0f}",
            delta_color=balance_color
        )
    
    with col4:
        if summary['total_income'] > 0:
            savings_rate = (summary['balance'] / summary['total_income']) * 100
            st.metric(
                label="貯蓄率",
                value=f"{savings_rate:.1f}%"
            )
        else:
            st.metric(label="貯蓄率", value="0%")
    
    # グラフ表示
    col1, col2 = st.columns(2)
    
    with col1:
        # 収支円グラフ
        if summary['total_income'] > 0 or summary['total_expense'] > 0:
            fig_pie = go.Figure(data=[go.Pie(
                labels=['収入', '支出'],
                values=[summary['total_income'], summary['total_expense']],
                hole=0.3,
                marker_colors=['#00ff00', '#ff0000']
            )])
            fig_pie.update_layout(title="収支比率")
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # カテゴリ別支出
        category_summary = db.get_category_summary(start_date, end_date)
        if not category_summary.empty:
            expense_data = category_summary[category_summary['transaction_type'] == 'expense']
            if not expense_data.empty:
                fig_bar = px.bar(
                    expense_data,
                    x='category',
                    y='amount',
                    title="カテゴリ別支出",
                    color='amount',
                    color_continuous_scale='Reds'
                )
                fig_bar.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_bar, use_container_width=True)

elif page == "➕ 収支記録":
    st.title("➕ 収支記録")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("日付", value=datetime.now())
            transaction_type = st.selectbox("収支タイプ", ["支出", "収入"])
            amount = st.number_input("金額", min_value=0, value=1000, step=100)
        
        with col2:
            # カテゴリの取得
            categories_df = db.get_categories("expense" if transaction_type == "支出" else "income")
            category = st.selectbox("カテゴリ", categories_df['name'].tolist())
            description = st.text_input("メモ")
        
        submitted = st.form_submit_button("記録を追加")
        
        if submitted:
            db.add_transaction(
                date.strftime("%Y-%m-%d"),
                category,
                description,
                amount,
                "expense" if transaction_type == "支出" else "income"
            )
            st.success("収支記録を追加しました！")

elif page == "📋 取引履歴":
    st.title("📋 取引履歴")
    
    # フィルター
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_type = st.selectbox("収支タイプ", ["全て", "収入", "支出"])
    
    with col2:
        start_date_filter = st.date_input("開始日", value=datetime.now() - timedelta(days=30))
    
    with col3:
        end_date_filter = st.date_input("終了日", value=datetime.now())
    
    # 取引履歴の取得
    transactions = db.get_transactions(
        start_date_filter.strftime("%Y-%m-%d"),
        end_date_filter.strftime("%Y-%m-%d")
    )
    
    if not transactions.empty:
        # フィルター適用
        if filter_type != "全て":
            filter_value = "income" if filter_type == "収入" else "expense"
            transactions = transactions[transactions['transaction_type'] == filter_value]
        
        # 表示用データの準備
        display_df = transactions.copy()
        display_df['収支タイプ'] = display_df['transaction_type'].map({
            'income': '収入',
            'expense': '支出'
        })
        display_df['金額'] = display_df['amount'].apply(lambda x: f"¥{x:,.0f}")
        display_df['日付'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d')
        
        # 表示列の選択
        display_columns = ['日付', 'category', 'description', '金額', '収支タイプ']
        display_df = display_df[display_columns]
        
        st.dataframe(display_df, use_container_width=True)
        
        # 削除機能
        st.subheader("取引の削除")
        if not transactions.empty:
            # 削除用の選択肢を作成
            delete_options = []
            for idx, row in transactions.iterrows():
                delete_options.append({
                    'id': row['id'],
                    'display': f"ID: {row['id']} - {row['date']} - {row['category']} - ¥{row['amount']:,.0f}"
                })
            
            selected_delete = st.selectbox(
                "削除する取引を選択",
                options=[opt['id'] for opt in delete_options],
                format_func=lambda x: next(opt['display'] for opt in delete_options if opt['id'] == x)
            )
            
            if st.button("削除"):
                db.delete_transaction(selected_delete)
                st.success("取引を削除しました！")
                st.rerun()
    else:
        st.info("指定された期間の取引履歴がありません。")

elif page == "📈 分析":
    st.title("📈 分析")
    
    # 期間選択
    col1, col2 = st.columns(2)
    with col1:
        analysis_period = st.selectbox(
            "分析期間",
            ["過去1ヶ月", "過去3ヶ月", "過去6ヶ月", "過去1年"]
        )
    
    # 期間の計算
    if analysis_period == "過去1ヶ月":
        days = 30
    elif analysis_period == "過去3ヶ月":
        days = 90
    elif analysis_period == "過去6ヶ月":
        days = 180
    else:
        days = 365
    
    start_date_analysis = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    end_date_analysis = datetime.now().strftime("%Y-%m-%d")
    
    # データ取得
    transactions = db.get_transactions(start_date_analysis, end_date_analysis)
    
    if not transactions.empty:
        # 月別収支推移
        transactions['date'] = pd.to_datetime(transactions['date'])
        transactions['month'] = transactions['date'].dt.to_period('M')
        
        monthly_summary = transactions.groupby(['month', 'transaction_type'])['amount'].sum().reset_index()
        monthly_pivot = monthly_summary.pivot(index='month', columns='transaction_type', values='amount').fillna(0)

        # income, expenseカラムが存在しない場合のエラーを回避
        if 'income' not in monthly_pivot.columns:
            monthly_pivot['income'] = 0
        if 'expense' not in monthly_pivot.columns:
            monthly_pivot['expense'] = 0

        monthly_pivot['balance'] = monthly_pivot['income'] - monthly_pivot['expense']
        
        # 月別収支グラフ
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=monthly_pivot.index.astype(str),
            y=monthly_pivot['income'],
            mode='lines+markers',
            name='収入',
            line=dict(color='green')
        ))
        fig_monthly.add_trace(go.Scatter(
            x=monthly_pivot.index.astype(str),
            y=monthly_pivot['expense'],
            mode='lines+markers',
            name='支出',
            line=dict(color='red')
        ))
        fig_monthly.add_trace(go.Scatter(
            x=monthly_pivot.index.astype(str),
            y=monthly_pivot['balance'],
            mode='lines+markers',
            name='収支バランス',
            line=dict(color='blue')
        ))
        
        fig_monthly.update_layout(
            title="月別収支推移",
            xaxis_title="月",
            yaxis_title="金額 (円)"
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
        
        # カテゴリ別分析
        col1, col2 = st.columns(2)
        
        with col1:
            # 支出カテゴリ別
            expense_by_category = transactions[transactions['transaction_type'] == 'expense'].groupby('category')['amount'].sum()
            if not expense_by_category.empty:
                expense_by_category = expense_by_category.sort_values(ascending=True)
                fig_expense = px.bar(
                    x=expense_by_category.values,
                    y=expense_by_category.index,
                    orientation='h',
                    title="カテゴリ別支出",
                    color=expense_by_category.values,
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_expense, use_container_width=True)
        
        with col2:
            # 収入カテゴリ別
            income_by_category = transactions[transactions['transaction_type'] == 'income'].groupby('category')['amount'].sum()
            if not income_by_category.empty:
                income_by_category = income_by_category.sort_values(ascending=True)
                fig_income = px.bar(
                    x=income_by_category.values,
                    y=income_by_category.index,
                    orientation='h',
                    title="カテゴリ別収入",
                    color=income_by_category.values,
                    color_continuous_scale='Greens'
                )
                st.plotly_chart(fig_income, use_container_width=True)
        
        # 統計情報
        st.subheader("統計情報")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_daily_expense = transactions[transactions['transaction_type'] == 'expense']['amount'].mean()
            st.metric("1日平均支出", f"¥{avg_daily_expense:,.0f}")
        
        with col2:
            avg_daily_income = transactions[transactions['transaction_type'] == 'income']['amount'].mean()
            st.metric("1日平均収入", f"¥{avg_daily_income:,.0f}")
        
        with col3:
            max_expense = transactions[transactions['transaction_type'] == 'expense']['amount'].max()
            st.metric("最大支出", f"¥{max_expense:,.0f}")
        
        with col4:
            max_income = transactions[transactions['transaction_type'] == 'income']['amount'].max()
            st.metric("最大収入", f"¥{max_income:,.0f}")
    
    else:
        st.info("分析期間のデータがありません。")

# フッター
st.sidebar.markdown("---")
st.sidebar.markdown("**家計簿アプリ v1.0**")
st.sidebar.markdown("Streamlit + SQLiteで作成") 