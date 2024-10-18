import os
from django.test import TestCase
from datetime import datetime
from news_sources.views import (
    scrape_verge,
    scrape_cnbctech,
    scrape_techcrunch,
    scrape_and_group_by_source,
    format_grouped_titles_by_source,
    scrape_all_news
)


# Directory to save output
output_dir = "testOutput"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Define current_date globally
current_date = datetime.now().date()

class ScraperIntegrationTests(TestCase):
    output_results = []  # Class variable to collect output

    @classmethod
    def tearDownClass(cls):
        # Write all output results to files after tests
        for filename, content in cls.output_results:
            file_path = os.path.join(output_dir, filename)
            with open(file_path, 'w') as file:
                file.write(content)

    def test_scrape_verge(self):
        articles = scrape_verge(current_date)
        
        output_content = f"Verge articles: {articles}\n"
        self.output_results.append(("verge_output.txt", output_content))
        
   
        self.assertTrue(len(articles) > 0, "No articles scraped from Verge")

    def test_scrape_cnbctech(self):
        articles = scrape_cnbctech(current_date)
        
        output_content = f"CNBC Tech articles: {articles}\n"
        self.output_results.append(("cnbc_output.txt", output_content))

      
        self.assertTrue(len(articles) > 0, "No articles scraped from CNBC Tech")

    def test_scrape_techcrunch(self):
        articles = scrape_techcrunch(current_date)
        
        output_content = f"TechCrunch articles: {articles}\n"
        self.output_results.append(("techcrunch_output.txt", output_content))

       
        self.assertTrue(len(articles) > 0, "No articles scraped from TechCrunch")

    def test_scrape_and_group_by_source(self):
        grouped_sources = scrape_and_group_by_source(current_date)
        
        output_content = f"Grouped news articles: {grouped_sources}\n"
        self.output_results.append(("grouped_sources_output.txt", output_content))

        
        self.assertTrue(len(grouped_sources) > 0, "No articles scraped and grouped by source")

    def test_format_grouped_titles_by_source(self):
        grouped_sources = scrape_and_group_by_source(current_date)
        formatted_text = format_grouped_titles_by_source(grouped_sources)
        
        output_content = f"Formatted text: {formatted_text}\n"
        self.output_results.append(("formatted_titles_output.txt", output_content))

       
        self.assertTrue(len(formatted_text) > 0, "No formatted news titles generated")

    def test_scrape_all_news(self):
        all_news = scrape_all_news(current_date)
        
        output_content = f"All scraped news: {all_news}\n"
        self.output_results.append(("all_news_output.txt", output_content))

       
        self.assertTrue(len(all_news) > 0, "No news articles scraped from all sources")

if __name__ == '__main__':
    import unittest
    unittest.main()
