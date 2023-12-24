from _cffi_backend import typeof
from sqlalchemy.orm import Session
from sqlalchemy import extract
from core import BaseRepo
from modules.report.entity import ReportEntity
import datetime


class DashboardRepository(BaseRepo):
    @staticmethod
    def dashboard_month(db: Session, year: int):
        data = db.query(ReportEntity).filter(extract('year', ReportEntity.reportedTime) == year)

        dataset = []
        xLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']

        if int(year) == datetime.datetime.now().year:
            for i in range(datetime.datetime.now().month):
                dataset.append(data.filter(extract('month', ReportEntity.reportedTime) == i + 1).count())
        else:
            for i in range(12):
                dataset.append(data.filter(extract('month', ReportEntity.reportedTime) == i + 1).count())

        return {
            'title': "Reports Per Month",
            'xLabels': xLabels,
            'dataset': dataset
        }

    @staticmethod
    def dashboard_year(db: Session):
        data = db.query(ReportEntity)

        # find all year in database
        year = []
        for i in range(len(data.all())):
            if data.all()[i].reportedTime.strftime("%Y") not in year:
                year.append(data.all()[i].reportedTime.strftime("%Y"))
        year.sort()

        # count reports per year
        dataset = []
        for i in range(len(year)):
            dataset.append(data.filter(extract('year', ReportEntity.reportedTime) == year[i]).count())

        return {
            'title': "Reports Per Year",
            'Year': year,
            'dataset': dataset
        }

    @staticmethod
    def dashboard_detail(db: Session):
        data = db.query(ReportEntity)

        reportdetail = [{"label": "all",
                         "number": data.count()},
                        {"label": "Approved",
                         "number": data.filter(ReportEntity.approval == True).count()},
                        {"label": "Done",
                            "number": data.filter(ReportEntity.completed == True).count()},
                        {"label": "Spam",
                         "number": data.filter(ReportEntity.spam == True).count()}]

        return {
            'reportDetail': reportdetail
        }

    @staticmethod
    def dashboard_category(db: Session):
        data = db.query(ReportEntity)

        category = []
        for i in range(len(data.all())):
            if data.all()[i].category not in category:
                category.append(data.all()[i].category)

        dataset = []
        for i in range(len(category)):
            dataset.append(data.filter(ReportEntity.category == category[i]).count())

        return {
            'title': "Trending Category",
            'xLabels': category,
            'datasets': dataset
        }

    @staticmethod
    def dashboard_solve(db: Session):
        data = db.query(ReportEntity).filter(ReportEntity.approval == True)

        dataset = []
        dataset.append(data.filter(ReportEntity.completed == True).count())
        dataset.append(data.filter(ReportEntity.completed == False).count())

        return {
            'title': "Solved Report",
            'xLabels': ["Solved", "In Progress"],
            'datasets': dataset
        }

    @staticmethod
    def dashboard_spam(db: Session):
        data = db.query(ReportEntity)

        dataset = []
        dataset.append(data.filter(ReportEntity.spam == True).count())
        dataset.append(data.filter(ReportEntity.spam == False).count())

        return {
            'title': "Spam Report",
            'xLabels': ["Spam", "Not Spam"],
            'datasets': dataset
        }