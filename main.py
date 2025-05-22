import argparse
import os
from collections import defaultdict
import datetime


def parse_csv(file_path: str) -> list[str: str]:
    result = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        res_keys = [key for key in lines[0].strip().split(',')]
        for line in lines[1:]:
            employee = dict(zip(res_keys, line.strip().split(',')))
            result.append(employee)
    return result

def generate_payout_report(data: list) -> None:

    department_data = defaultdict(list)

    for emp in data:
        emp_id: int = int(emp.pop('id', 'Unknown'))
        department: str = emp.pop('department', 'Unknown').capitalize()
        name: str = emp.pop('name', 'Unknown')
        hours: int = int(emp.pop('hours_worked', 0))
        email: str = emp.pop('email', 'Unknown')
        rate:int = int(list(emp.values())[0])
        payout = hours * rate

        department_data[department].append({
            'emp_id': emp_id,
            'email': email,
            'name': name,
            'hours': hours,
            'rate': rate,
            'payout': payout
        })


    print(f"{'departament':<12} | {'id':<4} | {'email':<20} | {'name':<20} | {'hours':<5} | {'rate':<4} | {'payout'}")
    print()
    for dept, records in department_data.items():
        print(dept.lower())
        total_hours = 0
        total_payout = 0
        for r in records:
            total_hours += r['hours']
            total_payout += r['payout']
            print(f"{'---':<12} | {r['emp_id']:<4} | {r['email']:<20} | {r['name']:<20} | {r['hours']:<5} | {r['rate']:<4} | ${r['payout']}")
        print(f"{'total':<12} | {'':<4} | {'':<20} | {'':<20} | {total_hours:<5} | {'':<4} | ${total_payout}")
        print()
    print(f"{'---':-<88}")


def main():
    parser = argparse.ArgumentParser(description='Generate employee reports.')
    parser.add_argument('files', nargs='+', help='Paths to CSV files with employee data')
    parser.add_argument('--report', required=True, help='Type of report to generate')

    args = parser.parse_args()
    # # Собираем всех сотрудников из файлов
    all_employees = []
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        all_employees.extend(parse_csv(file_path)) # .extend объединение всех работников в один лист

    # Карта возможных отчётов
    report_generators: dict = {
        'payout': generate_payout_report
    }

    report_type = args.report.lower()
    if report_type not in report_generators:
        print(f"Unsupported report type: {report_type}")
        return
    # Генерация нужного отчета
    report_generators[report_type](all_employees)


if __name__ == '__main__':
    main()
