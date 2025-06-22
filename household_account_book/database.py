import sqlite3
import pandas as pd
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="household_account.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベースとテーブルを初期化"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 収支記録テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # カテゴリテーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        
        # デフォルトカテゴリを追加
        default_categories = [
            ('食費', 'expense'),
            ('交通費', 'expense'),
            ('光熱費', 'expense'),
            ('通信費', 'expense'),
            ('娯楽費', 'expense'),
            ('医療費', 'expense'),
            ('教育費', 'expense'),
            ('給料', 'income'),
            ('ボーナス', 'income'),
            ('副業', 'income'),
            ('投資収益', 'income')
        ]
        
        for category, cat_type in default_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO categories (name, type) 
                VALUES (?, ?)
            ''', (category, cat_type))
        
        conn.commit()
        conn.close()
    
    def add_transaction(self, date, category, description, amount, transaction_type):
        """新しい取引を追加"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions (date, category, description, amount, transaction_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, category, description, amount, transaction_type))
        
        conn.commit()
        conn.close()
    
    def get_transactions(self, start_date=None, end_date=None):
        """取引履歴を取得"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM transactions"
        params = []
        
        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params = [start_date, end_date]
        elif start_date:
            query += " WHERE date >= ?"
            params = [start_date]
        elif end_date:
            query += " WHERE date <= ?"
            params = [end_date]
        
        query += " ORDER BY date DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_categories(self, transaction_type=None):
        """カテゴリを取得"""
        conn = sqlite3.connect(self.db_path)
        
        if transaction_type:
            query = "SELECT name FROM categories WHERE type = ?"
            df = pd.read_sql_query(query, conn, params=[transaction_type])
        else:
            query = "SELECT name, type FROM categories"
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        return df
    
    def get_summary(self, start_date=None, end_date=None):
        """収支サマリーを取得"""
        df = self.get_transactions(start_date, end_date)
        
        if df.empty:
            return {
                'total_income': 0,
                'total_expense': 0,
                'balance': 0,
                'income_count': 0,
                'expense_count': 0
            }
        
        income = df[df['transaction_type'] == 'income']['amount'].sum()
        expense = df[df['transaction_type'] == 'expense']['amount'].sum()
        
        return {
            'total_income': income,
            'total_expense': expense,
            'balance': income - expense,
            'income_count': len(df[df['transaction_type'] == 'income']),
            'expense_count': len(df[df['transaction_type'] == 'expense'])
        }
    
    def get_category_summary(self, start_date=None, end_date=None):
        """カテゴリ別サマリーを取得"""
        df = self.get_transactions(start_date, end_date)
        
        if df.empty:
            return pd.DataFrame()
        
        return df.groupby(['category', 'transaction_type'])['amount'].sum().reset_index()
    
    def delete_transaction(self, transaction_id):
        """取引を削除"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        
        conn.commit()
        conn.close() 