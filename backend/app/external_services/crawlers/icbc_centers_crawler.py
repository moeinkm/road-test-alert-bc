from typing import List, Dict
from datetime import datetime

import requests

from app.core.config import settings
from app.db.session import db_session_as_context
from app.models import Center
from app.external_services.crawlers import constants
from app.external_services.logging_config import setup_logging
from .icbc_login import get_auth_token

logger = setup_logging(__name__, log_file="icbc_centers_crawler.py")


class ICBCCentersCrawler:
    def run(self):
        try:
            data = self.scrape_icbc_locations()
            if not data:
                logger.error("No data returned from scrape_icbc_locations. Aborting update.")
                return
            with db_session_as_context() as db:
                for center in data:
                    try:
                        self.update_or_create(db, center)
                    except Exception as e:
                        logger.error(f"Failed to update or create center: {str(e)}")
        except Exception as e:
            logger.error(f"Error in run: {str(e)}")

    def scrape_icbc_locations(self) -> List[Dict]:
        """Scrape ICBC all locations."""
        url = settings.ICBC_TEST_CENTERS_LOCATION_URL
        exam_type = "5-R-1"
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Get authorization token
        auth_token = get_auth_token()
        if not auth_token:
            logger.error("Failed to retrieve Authorization token.")
            return []

        headers = {
            **constants.TEST_CENTERS_HEADERS,
            "Authorization": auth_token,
        }

        results = []
        for location in constants.TEST_LOCATIONS_TO_SCRAPE:
            city = location['city']
            lng = location['lng']
            lat = location['lat']

            body = {
                "lng": lng,
                "lat": lat,
                "examType": exam_type,
                "startDate": today_date
            }

            try:
                response = requests.put(url, headers=headers, json=body, timeout=10)
                response.raise_for_status()  # Raise HTTP error for bad responses (4xx or 5xx)
                data = response.json()
                logger.info(f"Appointments for {city}: {data}")
                if isinstance(data, list):
                    results.extend(data)
                else:
                    results.append(data)
            except requests.RequestException as e:
                logger.error(f"Failed to scrape data for {city}: {str(e)}")
                continue
        return results

    def update_or_create(self, db, center):
        """Save scraped data to the database."""
        try:
            center = db.query(Center).filter(Center.pos_id == center['pos']['posId']).first()
            # TODO: refactor to **dict for cleaner code this if block and else block
            if not center:
                center = Center(
                    pos_id=center['pos']['posId'],
                    name=center['pos']['agency'],
                    address=center['pos']['address'],
                    city=center['pos']['city'],
                    postal_code=center['pos']['postcode'],
                    lng=center['pos']['lng'],
                    lat=center['pos']['lat'],
                    url=center['pos']['url']
                )
                db.add(center)
                logger.info(f"Saved center with pos ID: {center['pos']['posId']}.")
            else:
                center.name = center['pos']['agency']
                center.address = center['pos']['address']
                center.city = center['pos']['city']
                center.postal_code = center['pos']['postcode']
                center.lng = center['pos']['lng']
                center.lat = center['pos']['lat']
                center.url = center['pos']['url']
                logger.info(f"Updated center with pos ID: {center['pos']['posId']}.")
            db.commit()
        except Exception as e:
            logger.error(f"Failed to save center with pos ID: {center.get('pos', {}).get('posId', 'UNKNOWN')}. Error: {str(e)}")
            db.rollback()

# Call the scraper
if __name__ == "__main__":
    icbc_crawler = ICBCCentersCrawler()
    icbc_crawler.run()
