from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_jobs: int
    total_companies: int
    total_locations: int
    total_sources: int


class CompanyResponse(BaseModel):
    company_id: int
    company_name: str
    total_jobs: int

class LocationResponse(BaseModel):
    location_id: int
    location_name: str
    total_jobs: int


class SourceResponse(BaseModel):
    source_id: int
    source_name: str
    total_jobs: int


class TrendResponse(BaseModel):
    date_posted: str
    total_jobs: int


class JobResponse(BaseModel):
    job_id: int
    title: str
    company: str
    location: str
    source: str
    date_posted: str
    description: str
    link: str