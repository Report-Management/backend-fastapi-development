from sqlalchemy.orm import Session
from sqlalchemy import extract, func, distinct
from core import BaseRepo, ResponseSchema
from modules.report.entity import ReportEntity
from core import ResponseSchema
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from itertools import groupby


class DashboardRepository(BaseRepo):
    @staticmethod
    def dashboard_month(db: Session, year: int):
        data = db.query(ReportEntity).filter(extract('year', ReportEntity.reportedTime) == year)

        current_month = datetime.datetime.now().month
        months_range = range(1, current_month + 1) if int(year) == datetime.datetime.now().year else range(1, 13)

        dataset = [data.filter(extract('month', ReportEntity.reportedTime) == i).count() for i in months_range]
        xLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
        month = [xLabels[i - 1] for i in months_range]

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
        data = db.query(extract('year', ReportEntity.reportedTime).label('year'), func.count().label('count')).group_by(
            extract('year', ReportEntity.reportedTime)).all()

        years = [str(row.year) for row in data]
        dataset = [row.count for row in data]

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                'title': "Reports Per Year",
                'xLabels': years,
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

        # Use distinct to get unique categories directly from the database
        categories = db.query(ReportEntity.category).distinct().all()
        category_names = [category[0] for category in categories]

        # Use func.count and group_by to get counts for each category in a single query
        dataset = db.query(ReportEntity.category, func.count(ReportEntity.category)).group_by(
            ReportEntity.category).all()
        dataset_counts = [count for category, count in dataset]

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Trending Category",
                    'xLabels': category_names,
                    'datasets': dataset_counts
                    }
        )

    @staticmethod
    def dashboard_category_year(db: Session, year: int):
        # Use distinct to get unique categories directly from the database
        categories = db.query(ReportEntity.category).filter(
            extract('year', ReportEntity.reportedTime) == year).distinct().all()
        category_names = [category[0] for category in categories]

        # Use func.count and group_by to get counts for each category in a single query
        dataset = (
            db.query(ReportEntity.category, func.count(ReportEntity.category))
            .filter(extract('year', ReportEntity.reportedTime) == year)
            .group_by(ReportEntity.category)
            .all()
        )
        dataset_counts = [count for category, count in dataset]

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={'title': "Trending Category",
                    'xLabels': category_names,
                    'datasets': dataset_counts
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

        # Find all unique years in the database
        years = db.query(extract('year', ReportEntity.reportedTime)).distinct().all()
        years = [int(year[0]) for year in years]
        years.sort()
        years.append(0)

        # Get all months of this year
        months = ["All", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        this_year = datetime.datetime.now().year
        this_month = datetime.datetime.now().month

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                'thisYear': this_year,
                'allYear': years,
                'thisMonth': months[:this_month + 1]
            }
        )