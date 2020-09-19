import urllib
import urllib2
import json

PROJECT_API_KEY = "AIzaSyCUukdto15Ad2PYZhlIVUSqQLUnqLYWti8"
RESULTS_LIMIT = 5
KNOWLEDGE_GRAPH_URL = "https://kgsearch.googleapis.com/v1/entities:search"
CONFIDENCE_THRESHOLD = 500.0

# ============    Call this function 'get_keyword_description_and_image'   ============
# keyword = string containing keyword entity
# printing = boolean option determining whether to print KG results to console (False by default)
# =====================================================================================
def get_keyword_description_and_image(keyword, printing=False):
	params = {"query" : keyword, "limit" : RESULTS_LIMIT, "key" : PROJECT_API_KEY}
	GET_request = KNOWLEDGE_GRAPH_URL + "?" + urllib.urlencode(params)
	try:
		json_response = urllib2.urlopen(GET_request)
	except urllib2.URLError as e:
		if hasattr(e, "reason"):
			print(" !! Failed to reach a server !!")
			print(" Reason:", e.reason)
		elif hasattr(e, "code"):
			print(" !! KG server could not fulfill the request for keyword:", keyword, "!!")
			print(" Error code:", e.code)
	else:
		raw_json_string = json_response.read()
		structured_response = json.loads(raw_json_string)
		try:
			item_list = structured_response["itemListElement"]
			if printing:
				print "keyword:", keyword
				print "num results:", len(item_list)
				print "conf:", item_list[0]["resultScore"]
			if len(item_list) > 0 and item_list[0]["resultScore"] > CONFIDENCE_THRESHOLD:
				smart_data = {}
				top_results = item_list[0]["result"]
				smart_data["proper_name"] = top_results["name"]
				if "image" in top_results and "contentUrl" in top_results["image"]:
					smart_data["image_url"] = top_results["image"]["contentUrl"]
				if "description" in top_results:
					smart_data["what_is_term"] = top_results["description"]
				if "detailedDescription" in top_results:
					smart_data["description"] = top_results["detailedDescription"]["articleBody"]
					smart_data["wikipedia_link"] = top_results["detailedDescription"]["url"]
				if printing:
					print smart_data
				return smart_data
		except Exception as e:
			print(" JSON Parsing Error: required data field missing ")
	return None
	

# Testing with different keywords
test_terms = []
#test_terms = ["mitosis", "halloween", "george washington carver", "french revolution", "pyroxene"]
for term in test_terms:
	get_keyword_description_and_image(term, printing=True)
	print ""
