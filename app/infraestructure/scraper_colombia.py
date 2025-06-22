import logging
import pandas as pd
from bs4 import BeautifulSoup
from typing import List
from app.config import load_config
from app.utils import send_requests
from app.domain import Country

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

config = load_config("colombia")
BASE_URL = config["base_url"]
PAGE_URL = config["page_url"]
SELECTORS = config["selectors"]
TABLE_SELECTOR = SELECTORS["table"]


class ColombiaSenadoScraper():
    def __init__(self,):
        pass

    def extract_project_links(self, soup: BeautifulSoup, table_selector: str, base_url:str) -> List[str]:
        links = []
        table = soup.select_one(table_selector)

        if table is None:
            logger.info("No se encontró la tabla. Fin del scraping.")
            return links
        
        rows = table.find_all("tr")[1:]

        for row in rows:
            cols = row.find_all("td")
            if not cols:
                continue

            a_tag = cols[2].find("a", href=True)

            if a_tag:
                href = a_tag["href"]
                full_url = base_url+href
                links.append(full_url)

        return links

    def parse_project_detail(self,soup: str) -> dict:
        data = {}

        estado_tag = soup.select_one("div.peractcom.proleyintestado")
        data["Estado"] = estado_tag.get_text(strip=True) if estado_tag else ""

        for block in soup.select("div.contpl"):
            labels = block.find_all(["div", "span"], class_="titlepl")
            if not labels:
                continue

            key = " ".join([lbl.get_text(strip=True).replace(":", "") for lbl in labels])
            for lbl in labels:
                lbl.extract()

            value = block.get_text(strip=True)
            data[key] = value if value else ""

            a_tag = block.find("a", href=True, string=lambda x: "ver documento" in x.lower())
            if a_tag:
                data["pdf"] = a_tag["href"]

        return data
    
    def scrape_colombia_laws(self,) -> pd.DataFrame:
        rows = []
        page_number = 0
        projects_links = []

        while True:
            url = f"{PAGE_URL}{page_number}"
            logger.info(f"Recolectando links - página {page_number}: {url}")
            soup = send_requests(url)

            detail_links = self.extract_project_links(soup=soup, table_selector=TABLE_SELECTOR, base_url=BASE_URL)
            if not detail_links:
                logger.info("No hay más links en esta página.")
                break

            projects_links.extend(detail_links)
            page_number += 1

        logger.info(f"Total de links recolectados: {len(projects_links)}")

        for index, link in enumerate(projects_links):
            logger.info(f"cogiendo info de {index}, projecto: {link}")
            try:
                project_detail = send_requests(link)
                parsed_data = self.parse_project_detail(project_detail)

                row = {
                    "id": f"colombia_{hash(parsed_data.get('Título', ''))}",
                    "country": Country.COLOMBIA.value,
                    "title": parsed_data.get("Título", ""),
                    "objecto_projecto": parsed_data.get("Objeto de proyecto", ""),
                    "filing_date": parsed_data.get("Fecha de radicación Cámara", ""),
                    "status": parsed_data.get("Estado", ""),
                    "pdf_links": BASE_URL + parsed_data["pdf"] if parsed_data.get("pdf") else "",
                    "source": link
                }
                rows.append(row)

            except Exception as e:
                logger.warning(f"Error procesando {link}: {e}")

        df= pd.DataFrame(rows)

        return df
