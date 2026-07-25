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