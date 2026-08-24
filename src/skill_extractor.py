import re


# =========================================================
# COMMON / CROSS-DOMAIN SKILLS
# =========================================================

COMMON_SKILLS = [
    "Microsoft Excel",
    "Excel",
    "Microsoft Word",
    "Microsoft PowerPoint",
    "MS Office",
    "Google Sheets",
    "Communication",
    "Leadership",
    "Team Management",
    "Project Management",
    "Problem Solving",
    "Time Management",
    "Customer Service",
    "Data Analysis",
    "Research",
    "Documentation",
    "Quality Control",
    "Quality Assurance",
    "Business Analysis",
]


# =========================================================
# MULTI-DOMAIN SKILL DATABASE
# =========================================================

DOMAIN_SKILLS = {

    # -----------------------------------------------------
    # COMPUTER SCIENCE / IT
    # -----------------------------------------------------

    "Computer Science / IT": [

        "Python",
        "Java",
        "JavaScript",
        "TypeScript",
        "C++",
        "C#",
        "PHP",
        "HTML",
        "CSS",
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",
        "Flask",
        "Django",
        "FastAPI",
        "React",
        "React Native",
        "Node.js",
        "Express.js",
        "Spring Boot",
        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Natural Language Processing",
        "Computer Vision",
        "Generative AI",
        "LLM",
        "Prompt Engineering",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "OpenCV",
        "Power BI",
        "Tableau",
        "Git",
        "GitHub",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "Google Cloud",
        "REST API",
        "API Development",
        "Data Structures",
        "Algorithms",
        "Cybersecurity",
        "Network Security",
        "Linux",
        "DevOps",
        "CI/CD",
        "Data Engineering",
        "Data Science",
        "Cloud Computing",
        "Database Management",
    ],


    # -----------------------------------------------------
    # MECHANICAL
    # -----------------------------------------------------

    "Mechanical Engineering": [

        "AutoCAD",
        "SolidWorks",
        "CATIA",
        "Creo",
        "ANSYS",
        "Fusion 360",
        "NX",
        "GD&T",
        "CAD",
        "CAM",
        "CAD/CAM",
        "CNC",
        "CNC Programming",
        "Machining",
        "Thermodynamics",
        "Fluid Mechanics",
        "Heat Transfer",
        "HVAC",
        "Machine Design",
        "Engineering Drawing",
        "Manufacturing Processes",
        "Finite Element Analysis",
        "FEA",
        "Mechanical Design",
        "Product Design",
        "Maintenance Engineering",
        "Hydraulics",
        "Pneumatics",
        "Metrology",
        "Material Science",
        "Robotics",
    ],


    # -----------------------------------------------------
    # ELECTRICAL
    # -----------------------------------------------------

    "Electrical Engineering": [

        "PLC",
        "SCADA",
        "MATLAB",
        "Simulink",
        "AutoCAD Electrical",
        "Electrical Machines",
        "Power Systems",
        "Power Electronics",
        "Circuit Analysis",
        "Control Systems",
        "Electrical Design",
        "Electrical Maintenance",
        "Transformers",
        "Switchgear",
        "Protection Systems",
        "Motor Control",
        "VFD",
        "Relay",
        "Solar Power",
        "Renewable Energy",
        "Industrial Automation",
        "Electrical Wiring",
        "Electrical Testing",
        "Power Distribution",
    ],


    # -----------------------------------------------------
    # ELECTRONICS / ECE
    # -----------------------------------------------------

    "Electronics & Communication": [

        "Embedded Systems",
        "Arduino",
        "Raspberry Pi",
        "IoT",
        "VLSI",
        "Verilog",
        "VHDL",
        "PCB Design",
        "Proteus",
        "MATLAB",
        "Simulink",
        "Microcontrollers",
        "Microprocessors",
        "Digital Electronics",
        "Analog Electronics",
        "Signal Processing",
        "Communication Systems",
        "RF",
        "FPGA",
        "Sensors",
        "Circuit Design",
        "Electronics Testing",
        "Internet of Things",
    ],


    # -----------------------------------------------------
    # CIVIL
    # -----------------------------------------------------

    "Civil Engineering": [

        "AutoCAD",
        "STAAD Pro",
        "ETABS",
        "Revit",
        "Civil 3D",
        "Primavera",
        "MS Project",
        "Surveying",
        "Quantity Estimation",
        "Quantity Surveying",
        "Construction Management",
        "Structural Engineering",
        "Structural Analysis",
        "Concrete Technology",
        "Geotechnical Engineering",
        "Transportation Engineering",
        "Environmental Engineering",
        "Building Planning",
        "Site Engineering",
        "Estimation and Costing",
        "BIM",
        "Project Planning",
    ],


    # -----------------------------------------------------
    # AUTOMOBILE
    # -----------------------------------------------------

    "Automobile Engineering": [

        "Automotive Engineering",
        "Vehicle Dynamics",
        "Automobile Design",
        "CATIA",
        "SolidWorks",
        "AutoCAD",
        "ANSYS",
        "IC Engine",
        "Engine Maintenance",
        "Vehicle Diagnostics",
        "Automotive Electronics",
        "Transmission Systems",
        "Suspension Systems",
        "Brake Systems",
        "EV Technology",
        "Electric Vehicles",
        "Automobile Maintenance",
        "Manufacturing",
        "CAD",
        "CNC",
    ],


    # -----------------------------------------------------
    # CHEMICAL
    # -----------------------------------------------------

    "Chemical Engineering": [

        "Aspen Plus",
        "Aspen HYSYS",
        "Process Engineering",
        "Process Design",
        "Chemical Process",
        "Mass Transfer",
        "Heat Transfer",
        "Fluid Mechanics",
        "Reaction Engineering",
        "Process Control",
        "Chemical Safety",
        "Plant Design",
        "P&ID",
        "Quality Control",
        "Laboratory Analysis",
        "MATLAB",
        "Process Simulation",
        "Petrochemical",
    ],


    # -----------------------------------------------------
    # BIOTECH / LIFE SCIENCE
    # -----------------------------------------------------

    "Biotechnology / Life Sciences": [

        "Biotechnology",
        "Bioinformatics",
        "PCR",
        "DNA Extraction",
        "Gel Electrophoresis",
        "Microbiology",
        "Molecular Biology",
        "Cell Culture",
        "Biochemistry",
        "Genetics",
        "Laboratory Techniques",
        "Research Methodology",
        "Clinical Research",
        "Data Analysis",
        "R Programming",
        "Python",
        "Genomics",
        "Protein Analysis",
    ],


    # -----------------------------------------------------
    # PRODUCTION / MANUFACTURING
    # -----------------------------------------------------

    "Production / Manufacturing": [

        "Lean Manufacturing",
        "Six Sigma",
        "5S",
        "Kaizen",
        "CNC",
        "Production Planning",
        "Production Management",
        "Quality Control",
        "Quality Assurance",
        "Process Improvement",
        "Industrial Engineering",
        "Manufacturing",
        "Inventory Management",
        "Supply Chain",
        "ISO",
        "Root Cause Analysis",
        "FMEA",
        "OEE",
        "TPM",
        "SAP",
    ],


    # -----------------------------------------------------
    # AEROSPACE
    # -----------------------------------------------------

    "Aerospace / Aeronautical Engineering": [

        "Aerodynamics",
        "Aircraft Structures",
        "Propulsion",
        "Flight Mechanics",
        "Aircraft Design",
        "CATIA",
        "SolidWorks",
        "ANSYS",
        "CFD",
        "MATLAB",
        "Avionics",
        "Aerospace Engineering",
        "Finite Element Analysis",
        "Thermodynamics",
        "Fluid Dynamics",
    ],


    # -----------------------------------------------------
    # MARINE
    # -----------------------------------------------------

    "Marine Engineering": [

        "Marine Engineering",
        "Marine Engines",
        "Marine Maintenance",
        "Ship Machinery",
        "Marine Electrical Systems",
        "Hydraulics",
        "Pneumatics",
        "Ship Design",
        "Naval Architecture",
        "Marine Safety",
        "Engine Maintenance",
        "Thermodynamics",
    ],


    # -----------------------------------------------------
    # ARCHITECTURE
    # -----------------------------------------------------

    "Architecture": [

        "AutoCAD",
        "Revit",
        "SketchUp",
        "Lumion",
        "3ds Max",
        "V-Ray",
        "BIM",
        "Architectural Design",
        "Building Design",
        "Interior Design",
        "Urban Planning",
        "Rendering",
        "Adobe Photoshop",
        "Adobe Illustrator",
        "Rhino",
    ],


    # -----------------------------------------------------
    # AGRICULTURE
    # -----------------------------------------------------

    "Agriculture": [

        "Agriculture",
        "Agronomy",
        "Soil Science",
        "Horticulture",
        "Crop Management",
        "Irrigation",
        "Farm Management",
        "Agricultural Engineering",
        "Plant Pathology",
        "Entomology",
        "Agricultural Economics",
        "Organic Farming",
        "Precision Agriculture",
        "GIS",
    ],


    # -----------------------------------------------------
    # ACCOUNTING / COMMERCE
    # -----------------------------------------------------

    "Commerce / Accounting": [

        "Accounting",
        "Tally",
        "Tally ERP",
        "Tally Prime",
        "GST",
        "Taxation",
        "Bookkeeping",
        "Financial Accounting",
        "Cost Accounting",
        "Auditing",
        "Payroll",
        "Accounts Payable",
        "Accounts Receivable",
        "Bank Reconciliation",
        "Microsoft Excel",
        "SAP",
        "QuickBooks",
    ],


    # -----------------------------------------------------
    # FINANCE
    # -----------------------------------------------------

    "Finance": [

        "Financial Analysis",
        "Financial Modeling",
        "Investment Analysis",
        "Portfolio Management",
        "Equity Research",
        "Valuation",
        "Risk Management",
        "Corporate Finance",
        "Banking",
        "Budgeting",
        "Forecasting",
        "Excel",
        "Power BI",
        "Bloomberg",
        "Accounting",
    ],


    # -----------------------------------------------------
    # MARKETING / SALES
    # -----------------------------------------------------

    "Marketing / Sales": [

        "Digital Marketing",
        "SEO",
        "SEM",
        "Google Ads",
        "Meta Ads",
        "Social Media Marketing",
        "Content Marketing",
        "Email Marketing",
        "Google Analytics",
        "Sales",
        "Business Development",
        "Lead Generation",
        "CRM",
        "Salesforce",
        "Market Research",
        "Brand Management",
        "Customer Relationship Management",
    ],


    # -----------------------------------------------------
    # HUMAN RESOURCES
    # -----------------------------------------------------

    "Human Resources": [

        "Recruitment",
        "Talent Acquisition",
        "HR Operations",
        "Payroll",
        "Employee Engagement",
        "Performance Management",
        "Training and Development",
        "HR Analytics",
        "HRMS",
        "Onboarding",
        "Employee Relations",
        "Human Resource Management",
        "Workforce Planning",
    ],


    # -----------------------------------------------------
    # OPERATIONS / SUPPLY CHAIN
    # -----------------------------------------------------

    "Operations / Supply Chain": [

        "Supply Chain Management",
        "Logistics",
        "Inventory Management",
        "Procurement",
        "Vendor Management",
        "Warehouse Management",
        "Operations Management",
        "SAP",
        "ERP",
        "Demand Planning",
        "Production Planning",
        "Lean",
        "Six Sigma",
        "Transportation Management",
    ],


    # -----------------------------------------------------
    # UI UX / GRAPHIC DESIGN
    # -----------------------------------------------------

    "Design / UI UX": [

        "UI Design",
        "UX Design",
        "UI/UX",
        "Figma",
        "Adobe XD",
        "Adobe Photoshop",
        "Adobe Illustrator",
        "Canva",
        "Wireframing",
        "Prototyping",
        "User Research",
        "Graphic Design",
        "Visual Design",
        "Interaction Design",
        "Design Thinking",
    ],


    # -----------------------------------------------------
    # HOSPITALITY
    # -----------------------------------------------------

    "Hospitality / Tourism": [

        "Hotel Management",
        "Front Office",
        "Food and Beverage",
        "Housekeeping",
        "Guest Relations",
        "Hospitality Management",
        "Customer Service",
        "Reservation Management",
        "Tourism Management",
        "Event Management",
        "Restaurant Operations",
    ],


    # -----------------------------------------------------
    # HEALTHCARE / NURSING
    # -----------------------------------------------------

    "Healthcare / Nursing": [

        "Patient Care",
        "Nursing",
        "Clinical Care",
        "Vital Signs",
        "Hospital Administration",
        "Healthcare Management",
        "Medical Documentation",
        "Patient Management",
        "First Aid",
        "Emergency Care",
        "Infection Control",
        "Clinical Documentation",
        "Ward Management",
    ],


    # -----------------------------------------------------
    # PHARMACY
    # -----------------------------------------------------

    "Pharmacy": [

        "Pharmacology",
        "Pharmaceutics",
        "Pharmaceutical Chemistry",
        "Clinical Pharmacy",
        "Drug Safety",
        "Pharmacovigilance",
        "Quality Assurance",
        "Quality Control",
        "GMP",
        "Drug Formulation",
        "Regulatory Affairs",
        "Clinical Research",
    ],


    # -----------------------------------------------------
    # EDUCATION
    # -----------------------------------------------------

    "Teaching / Education": [

        "Teaching",
        "Lesson Planning",
        "Curriculum Development",
        "Classroom Management",
        "Student Assessment",
        "Educational Technology",
        "Online Teaching",
        "Training",
        "Mentoring",
        "Instructional Design",
        "Academic Research",
    ],


    # -----------------------------------------------------
    # LAW
    # -----------------------------------------------------

    "Law / Legal": [

        "Legal Research",
        "Legal Drafting",
        "Contract Drafting",
        "Corporate Law",
        "Civil Law",
        "Criminal Law",
        "Legal Compliance",
        "Litigation",
        "Case Analysis",
        "Legal Documentation",
        "Intellectual Property",
        "Arbitration",
    ],


    # -----------------------------------------------------
    # ITI / TECHNICAL TRADES
    # -----------------------------------------------------

    "ITI / Technical Trades": [

        "Electrician",
        "Fitter",
        "Welder",
        "Welding",
        "MIG Welding",
        "TIG Welding",
        "Machinist",
        "Turner",
        "CNC Operator",
        "Maintenance Technician",
        "Mechanical Technician",
        "Electrical Technician",
        "Wireman",
        "Plumber",
        "Diesel Mechanic",
        "Motor Mechanic",
        "Refrigeration",
        "Air Conditioning",
        "HVAC",
        "Draftsman",
        "Carpentry",
        "Fabrication",
    ],
}


# =========================================================
# DOMAIN KEYWORDS
# Strong signals used for local domain detection.
# =========================================================

DOMAIN_KEYWORDS = {

    "Computer Science / IT": [
        "computer science",
        "information technology",
        "software engineering",
        "artificial intelligence",
        "machine learning",
        "data science",
        "cybersecurity",
    ],

    "Mechanical Engineering": [
        "mechanical engineering",
        "mechanical engineer",
    ],

    "Electrical Engineering": [
        "electrical engineering",
        "electrical engineer",
    ],

    "Electronics & Communication": [
        "electronics engineering",
        "electronics and communication",
        "ece",
        "embedded systems",
    ],

    "Civil Engineering": [
        "civil engineering",
        "civil engineer",
    ],

    "Automobile Engineering": [
        "automobile engineering",
        "automotive engineering",
    ],

    "Chemical Engineering": [
        "chemical engineering",
        "chemical engineer",
    ],

    "Biotechnology / Life Sciences": [
        "biotechnology",
        "life sciences",
        "bioinformatics",
    ],

    "Production / Manufacturing": [
        "production engineering",
        "manufacturing engineering",
        "industrial engineering",
    ],

    "Aerospace / Aeronautical Engineering": [
        "aerospace engineering",
        "aeronautical engineering",
    ],

    "Marine Engineering": [
        "marine engineering",
        "naval architecture",
    ],

    "Architecture": [
        "architecture",
        "architectural design",
    ],

    "Agriculture": [
        "agriculture",
        "agronomy",
    ],

    "Commerce / Accounting": [
        "commerce",
        "accounting",
        "accountant",
    ],

    "Finance": [
        "finance",
        "financial analyst",
        "banking",
    ],

    "Marketing / Sales": [
        "marketing",
        "sales",
        "business development",
    ],

    "Human Resources": [
        "human resources",
        "hr management",
        "talent acquisition",
    ],

    "Operations / Supply Chain": [
        "supply chain",
        "operations management",
        "logistics",
    ],

    "Design / UI UX": [
        "ui ux",
        "ui/ux",
        "graphic design",
        "product design",
    ],

    "Hospitality / Tourism": [
        "hotel management",
        "hospitality",
        "tourism",
    ],

    "Healthcare / Nursing": [
        "nursing",
        "healthcare",
        "patient care",
    ],

    "Pharmacy": [
        "pharmacy",
        "pharmaceutical",
    ],

    "Teaching / Education": [
        "teacher",
        "teaching",
        "education",
    ],

    "Law / Legal": [
        "law",
        "legal",
        "advocate",
    ],

    "ITI / Technical Trades": [
        "iti",
        "industrial training institute",
        "welder",
        "fitter",
        "electrician",
        "machinist",
    ],
}


# =========================================================
# TEXT MATCH HELPER
# =========================================================

def _contains_term(text, term):

    text = text.lower()
    term = term.lower()

    pattern = (
        r"(?<![a-zA-Z0-9])"
        +
        re.escape(term)
        +
        r"(?![a-zA-Z0-9])"
    )

    return bool(
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )
    )


# =========================================================
# REMOVE DUPLICATES WHILE KEEPING ORDER
# =========================================================

def _unique(items):

    seen = set()
    result = []

    for item in items:

        key = item.strip().lower()

        if key and key not in seen:

            seen.add(key)
            result.append(item.strip())

    return result


# =========================================================
# EXTRACT SKILLS LOCALLY
# =========================================================

def extract_skills(text):

    if not text:
        return []

    found = []


    # Common skills
    for skill in COMMON_SKILLS:

        if _contains_term(
            text,
            skill
        ):
            found.append(skill)


    # Domain skills
    for domain_skills in DOMAIN_SKILLS.values():

        for skill in domain_skills:

            if _contains_term(
                text,
                skill
            ):

                found.append(skill)


    return _unique(found)


# =========================================================
# DETECT DOMAIN LOCALLY
# =========================================================

def detect_domain_locally(text):

    if not text:
        return "General / Multidisciplinary"

    scores = {
        domain: 0
        for domain in DOMAIN_SKILLS
    }


    # Strong domain-name signals
    for domain, keywords in DOMAIN_KEYWORDS.items():

        for keyword in keywords:

            if _contains_term(
                text,
                keyword
            ):

                scores[domain] += 5


    # Skill-based signals
    for domain, skills in DOMAIN_SKILLS.items():

        for skill in skills:

            if _contains_term(
                text,
                skill
            ):

                scores[domain] += 1


    best_domain = max(
        scores,
        key=scores.get
    )


    if scores[best_domain] == 0:

        return "General / Multidisciplinary"


    return best_domain


# =========================================================
# MERGE LOCAL + AI SKILLS
# =========================================================

def merge_skills(
    local_skills,
    ai_skills
):

    local_skills = (
        local_skills
        if isinstance(local_skills, list)
        else []
    )

    ai_skills = (
        ai_skills
        if isinstance(ai_skills, list)
        else []
    )


    return _unique(
        local_skills
        +
        ai_skills
    )


# =========================================================
# SUPPORTED DOMAIN LIST
# =========================================================

def get_supported_domains():

    return list(
        DOMAIN_SKILLS.keys()
    )