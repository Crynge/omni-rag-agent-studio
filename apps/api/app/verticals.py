from __future__ import annotations

from collections import OrderedDict

SECTOR_VERTICALS: OrderedDict[str, list[str]] = OrderedDict(
    {
        "Retail & Commerce": [
            "Apparel Stores", "Footwear Brands", "Beauty Ecommerce", "Home Decor", "Pet Supplies",
            "Sporting Goods", "Luxury Retail", "Jewelry Stores", "Furniture Retail", "Toy Stores",
            "Consumer Electronics", "Office Supplies", "Grocery Delivery", "Pharmacy Retail",
            "Baby Products", "Subscription Boxes", "Marketplace Sellers", "Wholesale Distribution",
            "Flash Sale Brands", "Direct-to-Consumer Food"
        ],
        "Healthcare & Wellness": [
            "Hospitals", "Dental Clinics", "Dermatology Practices", "Physical Therapy Centers",
            "Mental Health Clinics", "Telemedicine Startups", "Medical Billing Firms", "Diagnostics Labs",
            "Wellness Coaches", "Fitness Studios", "Nutrition Brands", "Chiropractic Clinics",
            "Senior Care Services", "Home Health Agencies", "Medical Device Companies", "Pharmacies",
            "Optometry Clinics", "Veterinary Hospitals", "Fertility Clinics", "Rehabilitation Centers"
        ],
        "Financial Services": [
            "Retail Banking", "Credit Unions", "Insurance Brokers", "Wealth Advisors", "Tax Firms",
            "Bookkeeping Services", "Fintech Platforms", "Payment Processors", "Mortgage Brokers",
            "Payroll Providers", "Lending Platforms", "Crypto Services", "Accounting SaaS",
            "Risk Advisory Firms", "Expense Management Tools", "Invoice Factoring", "Treasury Tools",
            "Compliance Consultants", "Investment Research Firms", "Consumer Lending"
        ],
        "Legal & Compliance": [
            "Law Firms", "Employment Law Practices", "Immigration Consultancies", "Contract Review Teams",
            "IP Law Firms", "Legal Aid Services", "eDiscovery Teams", "Policy Compliance Offices",
            "Regulatory Advisory Firms", "Privacy Counsel", "Corporate Governance Teams", "ESG Compliance",
            "AML Teams", "Internal Audit", "Procurement Compliance", "Public Sector Compliance",
            "Healthcare Compliance", "Financial Compliance", "Safety Compliance", "Ethics Hotlines"
        ],
        "Education & Learning": [
            "K12 Schools", "Tutoring Platforms", "Higher Education", "EdTech SaaS", "Test Prep Brands",
            "Online Course Creators", "Corporate Learning", "Language Schools", "Training Academies",
            "STEM Camps", "Coding Bootcamps", "Library Services", "Learning Management Systems",
            "Special Education Providers", "Study Abroad Services", "Teacher Support Platforms",
            "Research Institutes", "Certification Programs", "Music Schools", "Career Coaching"
        ],
        "Real Estate & Property": [
            "Residential Brokerages", "Commercial Real Estate", "Property Management", "Vacation Rentals",
            "Title Services", "Mortgage Lead Gen", "Construction Sales", "Interior Design Studios",
            "Facility Management", "Coworking Spaces", "PropTech Platforms", "Home Inspection Services",
            "Real Estate Investment", "Senior Living Communities", "Student Housing", "HOA Services",
            "Land Development", "Architectural Firms", "Remodeling Contractors", "Solar Installers"
        ],
        "Travel & Hospitality": [
            "Hotels", "Resorts", "Boutique Stays", "Travel Agencies", "Tour Operators",
            "Destination Management", "Cruise Sales", "Airline Support", "Airport Services",
            "Vacation Planning", "Adventure Travel", "Restaurant Groups", "Cafes", "Cloud Kitchens",
            "Event Venues", "Wedding Venues", "Food Delivery Brands", "Hospitality Tech", "Nightlife", "Catering"
        ],
        "Technology & SaaS": [
            "B2B SaaS", "DevTools", "Cybersecurity", "IT Services", "Managed Service Providers",
            "Cloud Platforms", "Product Analytics", "CRM Vendors", "HR Tech", "Sales Tech",
            "Marketing Tech", "Customer Success Platforms", "API Platforms", "AI Startups",
            "Data Platforms", "Open Source Vendors", "Helpdesk Software", "No-Code Tools",
            "ERP Software", "Collaboration Tools"
        ],
        "Manufacturing & Industrial": [
            "Automotive Suppliers", "Electronics Manufacturing", "Food Manufacturing", "Textile Mills",
            "Chemical Plants", "Industrial Safety", "Packaging Firms", "Machinery Builders",
            "3D Printing Services", "Industrial IoT", "Warehouse Automation", "Mining Operations",
            "Oil & Gas Services", "Renewable Equipment", "Logistics Equipment", "Supply Chain Planning",
            "Aerospace Components", "Marine Manufacturing", "Industrial Training", "Quality Assurance Labs"
        ],
        "Media & Creative": [
            "Digital Publishers", "Marketing Agencies", "Creative Studios", "Video Production",
            "Podcast Networks", "PR Firms", "Influencer Agencies", "Gaming Studios", "Streaming Platforms",
            "Animation Houses", "Newsrooms", "Social Media Agencies", "Brand Consultancies", "Design Systems Teams",
            "Photography Services", "Music Labels", "Ad Operations", "Newsletter Businesses", "Community Platforms", "SEO Agencies"
        ],
        "Public Sector & Nonprofit": [
            "City Services", "Public Libraries", "Government Agencies", "Nonprofit Fundraising",
            "NGOs", "Public Health Agencies", "Civic Tech", "Grant Management", "Museum Operations",
            "Community Centers", "Relief Organizations", "Environmental Nonprofits", "Education Nonprofits",
            "Faith Organizations", "International Development", "Volunteer Networks", "Public Housing",
            "Transit Authorities", "State Programs", "Workforce Development"
        ],
        "Human Resources & People Ops": [
            "Recruiting Agencies", "Talent Acquisition Teams", "HR Outsourcing", "Benefits Administration",
            "Performance Management", "People Analytics", "Employee Onboarding", "Payroll Ops", "Learning & Development",
            "Internal Comms", "Executive Search", "Contract Staffing", "Employer Branding", "DEI Programs",
            "Remote Workforce Ops", "Labor Relations", "Career Services", "Internship Programs", "Freelancer Platforms", "Shift Scheduling"
        ],
        "Ecommerce Operations": [
            "Fulfillment Centers", "Returns Management", "Marketplace Operations", "Cross-Border Commerce",
            "Conversion Rate Optimization", "Customer Loyalty", "Email Retention", "SMS Marketing", "Affiliate Commerce",
            "Influencer Commerce", "Wholesale Portals", "Mobile Commerce", "Merchandising Teams", "Demand Planning",
            "Inventory Forecasting", "Order Management", "Fraud Prevention", "Customer Care", "Review Management", "Subscription Retention"
        ],
        "Professional Services": [
            "Consulting Firms", "Business Coaching", "Architecture Firms", "Engineering Consultancies",
            "Translation Services", "Virtual Assistant Firms", "BPO Services", "Procurement Advisory",
            "Market Research Firms", "Corporate Training", "Investor Relations", "Strategy Offices",
            "Board Advisory", "M&A Advisory", "Franchise Consulting", "Supply Chain Consulting",
            "Sustainability Advisory", "Design Consulting", "Operations Consulting", "Change Management"
        ],
        "Logistics & Mobility": [
            "Freight Brokers", "Last-Mile Delivery", "Courier Services", "Trucking Fleets", "Fleet Management",
            "Mobility Apps", "Ride Hailing", "Warehousing", "Cold Chain Logistics", "Import Export Firms",
            "Port Operations", "Rail Logistics", "Aviation Services", "Customs Brokerage", "Dispatch Operations",
            "Field Service Routing", "Maritime Logistics", "Vehicle Leasing", "Bicycle Delivery", "Supply Transport"
        ],
        "Consumer Services": [
            "Home Cleaning", "Laundry Services", "Pest Control", "Plumbing", "Electrical Contractors",
            "HVAC Services", "Landscaping", "Security Services", "Personal Care", "Spa Services",
            "Salon Chains", "Wedding Planning", "Pet Grooming", "Moving Services", "Repair Services",
            "Childcare Providers", "Elder Concierge", "Home Tutoring", "Personal Shopping", "Local Service Marketplaces"
        ]
    }
)


def slugify(value: str) -> str:
    return value.lower().replace("&", "and").replace("/", " ").replace("-", " ").replace("  ", " ").replace(" ", "-")


def build_vertical_profiles() -> list[dict[str, object]]:
    profiles: list[dict[str, object]] = []
    for sector, names in SECTOR_VERTICALS.items():
        for name in names:
            profiles.append(
                {
                    "slug": slugify(name),
                    "name": name,
                    "sector": sector,
                    "short_description": f"{name} teams need grounded AI answers, business-safe responses, and workflow-aware escalation paths.",
                    "common_use_cases": [
                        "customer support and FAQ",
                        "internal knowledge assistant",
                        "policy and compliance lookup",
                        "lead qualification or intake",
                    ],
                    "tone_guidance": "Answer with grounded confidence, cite sources, clarify uncertainty, and avoid pretending to know missing facts.",
                }
            )
    return profiles


ALL_VERTICAL_PROFILES = build_vertical_profiles()
ALL_VERTICAL_COUNT = len(ALL_VERTICAL_PROFILES)
VERTICAL_INDEX = {item["slug"]: item for item in ALL_VERTICAL_PROFILES}

