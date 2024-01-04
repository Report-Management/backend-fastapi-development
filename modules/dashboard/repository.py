from sqlalchemy.orm import Session
from sqlalchemy import extract
from core import BaseRepo, ResponseSchema
from modules.report.entity import ReportEntity
from core import ResponseSchema
import datetime
from fastapi import APIRouter, Depends, HTTPException, status


class DashboardRepository(BaseRepo):
    @staticmethod
    def dashboard_month(db: Session, year: int):
        data = db.query(ReportEntity).filter(extract('year', ReportEntity.reportedTime) == year)

        dataset = []
        xLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
        month = []

        if int(year) == datetime.datetime.now().year:
            for i in range(datetime.datetime.now().month):
                dataset.append(data.filter(extract('month', ReportEntity.reportedTime) == i + 1).count())
                month.append(xLabels[i])
        else:
            for i in range(12):
                dataset.append(data.filter(extract('month', ReportEntity.reportedTime) == i + 1).count())
                month.append(xLabels[i])

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                'title': "Reports Per Month",
                'xLabels': month,
                'datasets': dataset
            }
        )


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

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Reports Per Year",
                    'xLabels': year,
                    'datasets': dataset
                    }
        )

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

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'reportDetail': reportdetail
                    }
        )

    @staticmethod
    def dashboard_category_all(db: Session):
        data = db.query(ReportEntity)

        category = []
        for i in range(len(data.all())):
            if data.all()[i].category not in category:
                category.append(data.all()[i].category)

        dataset = []
        for i in range(len(category)):
            dataset.append(data.filter(ReportEntity.category == category[i]).count())

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Trending Category",
                    'xLabels': category,
                    'datasets': dataset
                    }
        )

    @staticmethod
    def dashboard_category_year(db: Session, year: int):
        data = db.query(ReportEntity).filter(extract('year', ReportEntity.reportedTime) == year)

        category = []
        for i in range(len(data.all())):
            if data.all()[i].category not in category:
                category.append(data.all()[i].category)

        dataset = []
        for i in range(len(category)):
            dataset.append(data.filter(ReportEntity.category == category[i]).count())

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Trending Category",
                    'xLabels': category,
                    'datasets': dataset
                    }
        )

    @staticmethod
    def dashboard_solve(db: Session, year: int, month: int):
        data = db.query(ReportEntity).filter(ReportEntity.approval == True)

        if int(year) != 0 and int(month) == 0:
            data = data.filter(extract('year', ReportEntity.reportedTime) == year)
        elif int(year) != 0 and int(month) != 0:
            data = data.filter(extract('year', ReportEntity.reportedTime) == year).filter(
                extract('month', ReportEntity.reportedTime) == month)
        elif int(year) == 0 and int(month) != 0:
            data = data.filter(extract('month', ReportEntity.reportedTime) == month)


        dataset = []
        dataset.append(data.filter(ReportEntity.completed == True).count())
        dataset.append(data.filter(ReportEntity.completed == False).count())

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Solved Report",
                    'xLabels': ["Solved", "In Progress"],
                    'datasets': dataset
                    }
        )

    @staticmethod
    def dashboard_spam(db: Session, year: int, month: int):
        if int(year) == 0 and int(month) == 0:
            data = db.query(ReportEntity)
        elif int(year) != 0 and int(month) == 0:
            data = db.query(ReportEntity).filter(extract('year', ReportEntity.reportedTime) == year)
        elif int(year) == 0 and int(month) != 0:
            data = db.query(ReportEntity).filter(extract('month', ReportEntity.reportedTime) == month)
        else:
            data = db.query(ReportEntity).filter(extract('year', ReportEntity.reportedTime) == year).filter(
                extract('month', ReportEntity.reportedTime) == month)

        dataset = []
        dataset.append(data.filter(ReportEntity.spam == True).count())
        dataset.append(data.filter(ReportEntity.spam == False).count())

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Spam Report",
                    'xLabels': ["Spam", "Not Spam"],
                    'datasets': dataset
                    }
        )

    @staticmethod
    def dashboard_date(db: Session):
        data = db.query(ReportEntity)

        # find all year in database
        year = []
        for i in range(len(data.all())):
            if int(data.all()[i].reportedTime.strftime("%Y")) not in year:
                year.append(int(data.all()[i].reportedTime.strftime("%Y")))
        year.sort()
        year.append(0)

        # get all month of this year
        months = ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                  "Oct", "Nov", "Dec"]
        month = []
        for i in range(int(datetime.datetime.now().month)+1):
            month.append(months[i])

        thisyear = datetime.datetime.now().year

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'thisYear': thisyear,
                    'allYear': year,
                    'thisMonth': month
                    }
        )