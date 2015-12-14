from elasticsearch import Elasticsearch
from elasticsearch import helpers

import requests
from bs4 import BeautifulSoup
import time

# websites to parse
websites = [
		# 'http://www.parents.com/pregnancy/my-body/nutrition/a-food-guide-for-pregnant-women/?socsrc=parentstw_20151027225000',
		# 'http://www.webmd.com/baby/features/foods-to-avoid-when-youre-pregnant',
		# 'http://www.webmd.com/baby/features/foods-to-avoid-when-youre-pregnant?page=2',
		# 'http://www.webmd.com/baby/features/foods-to-avoid-when-youre-pregnant?page=3',
		# 'http://www.webmd.com/baby/features/foods-to-avoid-when-youre-pregnant?page=4',
		# 'http://www.babycentre.co.uk/x568574/whats-not-safe-to-eat-in-pregnancy',
		# 'http://www.babycenter.com.au/x568574/what-isnt-safe-to-eat-during-pregnancy',
		# 'http://www.babycenter.com/0_eating-fish-during-pregnancy-how-to-avoid-mercury-and-still_10319861.bc?showAll=true',
		# 'http://americanpregnancy.org/pregnancy-health/foods-to-avoid-during-pregnancy/',
		# 'http://www.mayoclinic.org/healthy-lifestyle/pregnancy-week-by-week/in-depth/pregnancy-and-fish/art-20044185?pg=1',
		# 'http://www.mayoclinic.org/healthy-lifestyle/pregnancy-week-by-week/in-depth/pregnancy-and-fish/art-20044185?pg=2',
		# 'http://www.nhs.uk/chq/Pages/917.aspx?CategoryID=54#close',
		# 'http://www.todaysparent.com/pregnancy/being-pregnant/pregnancy-food-guide/',
		# 'http://www.netmums.com/pregnancy/staying-healthy-in-pregnancy/eating-in-pregnancy-do-s-don-ts',
		# 'http://www.foodauthority.nsw.gov.au/consumers/life-events-and-food/pregnancy/pregnancy-table#.VkqgXd-rRTY',
		# 'http://www.thebump.com/a/what-to-avoid-during-pregnancy-and-how-not-to-miss-it-too-much',
		# 'http://www.eatright.org/resource/health/pregnancy/what-to-eat-when-expecting/seafood-dos-and-donts-when-pregnant',
		# 'http://www.madeformums.com/pregnancy/are-mozzarella-halloumi-and-feta-safe-in-pregnancy/29571.html',
		# 'http://www.dietvsdisease.org/what-cant-you-eat-when-pregnant-6-foods-to-avoid/',
		# 'http://www.fitpregnancy.com/nutrition/prenatal-nutrition/should-you-eat-fish-during-pregnancy',
		# 'http://www.medscape.com/viewarticle/484035',
		# 'http://www.bellybelly.com.au/pregnancy/truth-about-what-you-can-eat-during-pregnancy/'
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-deli-meat-while-im-pregnant_1246923.bc',
		# 'http://www.babycenter.com/404_is-it-safe-for-pregnant-women-to-eat-meat-from-livestock-tha_1245310.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-fish-and-other-seafood-when-im-pregnant_1380503.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-sushi-while-pregnant_1245280.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-raw-oysters-during-pregnancy_1245282.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-fish-raw-or-seared-during-pregnancy_2284.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-a-lot-of-chocolate-during-pregnancy_1245156.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-soft-cheese-during-pregnancy_3175.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-binge-on-halloween-candy-while-im-pregnant_10323311.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-spicy-foods-during-pregnancy_1246919.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-a-lot-of-salty-foods-during-pregnancy_2348.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-use-artificial-sweeteners-during-pregnancy_9213.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-foods-with-msg-during-pregnancy_2285.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-blackened-foods-during-pregnancy_1246905.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-eat-cured-or-smoked-foods-while-im-pregnant_1246924.bc',
		# 'http://www.babycenter.com/0_holiday-foods-to-avoid-during-pregnancy_1408439.bc',
		# 'http://www.babycenter.com/pregnancy-eating-well',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-eggnog-during-pregnancy_10322.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-unpasteurized-juice-during-pregnancy_1246870.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-tap-water-when-im-pregnant_1246879.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-milk-from-cows-that-were-given-bst-while_1245308.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-herbal-tea-during-pregnancy_1246852.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-diet-soda-during-pregnancy_1245945.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-diet-shakes-during-pregnancy_1245309.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-have-my-morning-cup-of-coffee-during-pregnancy_1246893.bc',
		# 'http://www.babycenter.com/404_is-it-safe-to-drink-caffeinated-sodas-when-im-pregnant_1246871.bc',
		# 'http://www.babycenter.com/0_drinking-alcohol-during-pregnancy_3542.bc',
		# 'http://www.momjunction.com/articles/safe-eat-pizza-pregnancy_0022422/',
		# 'http://www.thekitchn.com/yes-pregnant-women-can-eat-good-cheese-pregnancysafe-cheese-ideas-for-a-baby-shower-the-cheesemonger-203864',
		# 'http://kimberlysnyder.com/blog/2012/02/07/what-foods-you-should-eat-and-not-eat-when-pregnant/',
		# 'http://www.livestrong.com/article/513885-is-it-safe-to-eat-hamburgers-while-pregnant/',
		# 'http://mom.girlstalkinsmack.com/health/can-you-eat-crab-meat-during-pregnancy-.aspx',
		# r'http://www.obfocus.com/questions/Can%%20Pregnant%%20Women%%20Eat%%20Crab.htm',
		# 'http://www.livestrong.com/article/315198-burdock-root-and-pregnancy/',
		]

es = Elasticsearch();

# will hold final list
all_data = []

# iterate through websites
for website in websites:
	r = requests.get(website)
	soup = BeautifulSoup(r.content, "html.parser")

	# stripping tags from HTML to create as much smooth, sentence-like text as possible
	[s.extract() for s in soup(['iframe', 'script', 'em','b','a'])]

	# tentatively only using p tags
	for tag in soup.find_all('p'):

		# text without the tags
		text = tag.text

		# forming JSON - seems important to make sure the data is a string
		data = {
				'_index' : 'pregnancy',
				'_type' : 'html',
				'_source' : {
					'source' : website,
					'text' : str(text),
					'boost' : 1
					}
			   }

		all_data.append(data)

# finally putting into elasticsearch using bulk API
helpers.bulk(es, all_data)
