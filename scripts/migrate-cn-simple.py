#!/usr/bin/env python3
"""
@file: migrate-cn-simple.py
@description: Простая миграция таблицы cn
@created: 2025-08-30
"""

import logging
import subprocess
import psycopg2
from datetime import datetime

class MigrateCNSimple:
    def __init__(self):
        self.setup_logging()
        self.pg_conn_str = "dbname=Fish_Eye user=postgres password=postgres host=localhost port=5432"
        self.pg_conn = None
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('migrate-cn-simple.log'),
                logging.StreamHandler()
            ]
        )
    
    def connect_postgres(self):
        """Подключение к PostgreSQL"""
        try:
            self.pg_conn = psycopg2.connect(self.pg_conn_str)
            logging.info("✅ Подключение к PostgreSQL успешно.")
            return True
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка подключения к PostgreSQL: {ex}")
            return False
    
    def get_cn_data(self):
        """Получение данных из SQL Server"""
        try:
            cmd = [
                "docker", "exec", "vuege-mssql",
                "/opt/mssql-tools18/bin/sqlcmd",
                "-S", "localhost,1433",
                "-U", "sa",
                "-P", "Vuege2024!",
                "-d", "Fish_Eye",
                "-Q", "SELECT cn_key, cn_number, cn_date, cn_note, cnMark, cnTimeOfEntry, cnName FROM ags.cn",
                "-C"
            ]
            
            logging.info("🔍 Получение данных из SQL Server: cn")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                data_lines = []
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('---') and not line.startswith('(') and not line.startswith('cn_key'):
                        data_lines.append(line)
                
                logging.info(f"📄 Получены данные из SQL Server: {len(data_lines)} строк")
                return data_lines
            else:
                logging.error(f"❌ Ошибка получения данных: {result.stderr}")
                return []
                
        except Exception as e:
            logging.error(f"❌ Ошибка получения данных: {e}")
            return []
    
    def parse_cn_line(self, line):
        """Парсинг строки данных cn"""
        try:
            # Фиксированные позиции для таблицы cn
            cn_key = line[0:11].strip()
            cn_number = line[11:266].strip()
            cn_date = line[266:282].strip()
            cn_note = line[282:448].strip()
            cnMark = line[448:459].strip()
            cnTimeOfEntry = line[459:481].strip()
            cnName = line[481:981].strip()
            
            return {
                'cn_key': int(cn_key) if cn_key and cn_key != 'NULL' else None,
                'cn_number': cn_number if cn_number and cn_number != 'NULL' else None,
                'cn_date': cn_date if cn_date and cn_date != 'NULL' else None,
                'cn_note': cn_note if cn_note and cn_note != 'NULL' else None,
                'cnMark': int(cnMark) if cnMark and cnMark != 'NULL' else None,
                'cnTimeOfEntry': cnTimeOfEntry if cnTimeOfEntry and cnTimeOfEntry != 'NULL' else None,
                'cnName': cnName if cnName and cnName != 'NULL' else None
            }
        except Exception as e:
            logging.error(f"❌ Ошибка парсинга строки: {line[:50]}... - {e}")
            return None
    
    def insert_cn_data(self, data_lines):
        """Вставка данных в PostgreSQL"""
        if not data_lines:
            logging.info("⚠️ Нет данных для вставки")
            return False
        
        pg_cursor = self.pg_conn.cursor()
        try:
            successful_inserts = 0
            
            for line in data_lines:
                if line.strip():
                    parsed_data = self.parse_cn_line(line)
                    
                    if parsed_data and parsed_data['cn_key'] is not None:
                        insert_sql = """
                        INSERT INTO ags.cn (cn_key, cn_number, cn_date, cn_note, cnMark, cnTimeOfEntry, cnName)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        
                        values = (
                            parsed_data['cn_key'],
                            parsed_data['cn_number'],
                            parsed_data['cn_date'],
                            parsed_data['cn_note'],
                            parsed_data['cnMark'],
                            parsed_data['cnTimeOfEntry'],
                            parsed_data['cnName']
                        )
                        
                        pg_cursor.execute(insert_sql, values)
                        successful_inserts += 1
            
            self.pg_conn.commit()
            logging.info(f"✅ Данные мигрированы: {successful_inserts} записей")
            return True
            
        except psycopg2.Error as ex:
            logging.error(f"❌ Ошибка вставки данных: {ex}")
            self.pg_conn.rollback()
            return False
    
    def validate_migration(self):
        """Валидация миграции"""
        pg_cursor = self.pg_conn.cursor()
        try:
            pg_cursor.execute("SELECT COUNT(*) FROM ags.cn")
            pg_count = pg_cursor.fetchone()[0]
            
            logging.info(f"✅ Валидация: {pg_count} записей в PostgreSQL")
            return pg_count > 0
                
        except Exception as ex:
            logging.error(f"❌ Ошибка валидации: {ex}")
            return False
    
    def run_migration(self):
        """Запуск миграции"""
        logging.info("🚀 Начало миграции таблицы cn")
        print("🚀 МИГРАЦИЯ ТАБЛИЦЫ CN")
        print("=" * 40)
        
        if not self.connect_postgres():
            return
        
        # Получение данных
        data_lines = self.get_cn_data()
        
        if not data_lines:
            print("⚠️ Нет данных для миграции")
            return
        
        # Вставка данных
        if self.insert_cn_data(data_lines):
            # Валидация
            if self.validate_migration():
                print("✅ Миграция завершена успешно!")
            else:
                print("⚠️ Ошибка валидации")
        else:
            print("❌ Ошибка вставки данных")
        
        self.pg_conn.close()

def main():
    """Основная функция"""
    print("🚀 Запуск простой миграции таблицы cn")
    
    migrator = MigrateCNSimple()
    migrator.run_migration()

if __name__ == "__main__":
    main()