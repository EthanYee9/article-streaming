def api_response_data():
    return {
        "response": {
            "status": "ok",
            "userTier": "developer",
            "total": 7408,
            "startIndex": 1,
            "pageSize": 10,
            "currentPage": 1,
            "pages": 741,
            "orderBy": "relevance",
            "results": [
                {
                    "id": "global-development/2025/aug/03/mountains-refugees-mountaineering-peace-friendship-alpine-climb",
                    "type": "article",
                    "sectionId": "global-development",
                    "sectionName": "Global development",
                    "webPublicationDate": "2025-08-03T12:00:40Z",
                    "webTitle": "Friendship at 13,000 feet: how climbing in the Swiss Alps is bringing refugees together",
                    "webUrl": "https://www.theguardian.com/global-development/2025/aug/03/mountains-refugees-mountaineering-peace-friendship-alpine-climb",
                    "apiUrl": "https://content.guardianapis.com/global-development/2025/aug/03/mountains-refugees-mountaineering-peace-friendship-alpine-climb",
                    "fields": {
                        "body": '<p>At 4,000 metres, conditions can be challenging. The air is thin, movement takes effort, and the ice and snow demand proper gear: warm layers, crampons, an ice axe, ropes for crossing glaciers.</p> <p>Yet a group of refugees in Switzerland \u2013 from Afghanistan, Iran, Palestine, Ukraine and elsewhere \u2013 say this is exactly where they have found freedom, calm and even respite from the trauma of war, political persecution and imprisonment.</p> <p>\u201cMountaineering isn\u2019t just a sport. Reaching the summit brings an incredible sense of relief. And it\u2019s proof that you can overcome your physical and emotional challenges, even after extreme hardship,\u201d says Soroush Esfandiary, 27, adding that the Alps remind him of growing up near Iran\u2019s Zagros mountains, but also of his escape from home.</p>    <p>Esfandiary arrived in Switzerland four years ago, initially crossing the mountains from Iran into Turkey on foot. \u201cI had a high fever and was coughing up blood, but I kept moving. I was so afraid,\u201d he says.</p> <p>After joining the <a href="https://www.theguardian.com/commentisfree/2019/nov/26/the-guardian-view-on-irans-protests-unrest-is-crushed-unhappiness-endures">mass protests in Iran in 2019</a>, initially sparked by a sudden surge in fuel prices, Esfandiary was imprisoned and put in solitary confinement for two weeks in Isfahan intelligence prison. When he was released to await his trial, he knew he had to leave.</p> <p>Soon after reaching Switzerland, Esfandiary joined <a href="https://www.peaks4all.org/">Peaks4All</a>, a Geneva-based non-profit that supports refugee integration through mountaineering.</p> <p>\u201cIt\u2019s more than mountaineering though,\u201d he explains. \u201cWe\u2019re a group of people from all over the world, connected by what we\u2019ve been through. We are all here in Switzerland to find peace.\u201d</p> <p>The idea of offering mountaineering to refugees in the Swiss Alps all started with two female mountaineers:</p> <p>\u201cWe came up with it because of our passion for Alpinism and social impact,\u201d says La\u00ebtitia Lam, who co-founded Peaks4All with her friend and fellow mountaineer Cl\u00e9mence Delloye.</p>    <p>\u201cWhat started as a one-off project with just a handful of people has grown into a community of more than 200 refugees from across the globe, from Nigeria and Sudan, to Mongolia, Turkey and Syria.'
                    },
                    "isHosted": False,
                    "pillarId": "pillar/news",
                    "pillarName": "News",
                }
            ],
        }
    }


def test_data_descending_publication_dates():
    return {
        "response": {
            "status": "ok",
            "results": [
                {
                    "webPublicationDate": "2025-09-16T16:22:48Z",
                    "webTitle": "How AI is undermining learning and teaching in universities | Letter",
                },
                {
                    "webPublicationDate": "2025-04-20T07:00:01Z",
                    "webTitle": "How a rip-off of Ukraine\u2019s Zorya Luhansk are climbing Russia\u2019s pyramid",
                },
                {
                    "webPublicationDate": "2025-06-21T08:00:03Z",
                    "webTitle": "10 of the best climbing plants for your garden, from honeysuckle to sweet pea",
                },
                {
                    "webPublicationDate": "2025-08-03T12:00:40Z",
                    "webTitle": "Friendship at 13,000 feet: how climbing in the Swiss Alps is bringing refugees together",
                },
            ],
        }
    }


def sample_articles():
    return [
        {
            "id": "music/2025/sep/21/busted-vs-mcfly-review-millenial-rivals-let-the-pop-rock-punches-fly",
            "type": "article",
            "sectionId": "music",
            "sectionName": "Music",
            "webPublicationDate": "2025-09-21T16:00:21Z",
            "webTitle": "Busted vs McFly review \u2013 millennial \u2018rivals\u2019 let the pop-rock punches fly",
            "webUrl": "https://www.theguardian.com/music/2025/sep/21/busted-vs-mcfly-review-millenial-rivals-let-the-pop-rock-punches-fly",
            "apiUrl": "https://content.guardianapis.com/music/2025/sep/21/busted-vs-mcfly-review-millenial-rivals-let-the-pop-rock-punches-fly",
            "fields": {
                "body": "<p>The last time Busted and McFly shared a stage a decade ago they were conjoined as McBusted, an unholy union that resulted in two arena tours and an album. Now they\u2019ve reconnected as pop-rock foes, with the \u201crivalry\u201d \u2013 both bands were formed by the same management company, with McFly arriving three years after Busted in 2003 \u2013 cemented by an opening video segment based on Baz Luhrmann\u2019s Romeo + Juliet that pits them as \u201cstar crossed bands\u201d living in \u201cfair Britannia\u201d. Millennial couples in rival Team Busted and Team McFly T-shirts, meanwhile, eye each other up nervously.</p> <p>A surprisingly buff McFly open proceedings, anchoring their rock credentials with 2023\u2019s Where Did All the Guitars Go?, an embarrassing \u201creal music\u201d diatribe about the \u201cshit\u201d on the radio. But while there are some other duds in their 12 song set \u2013 Red is a Kidz Bop version of U2; the faux-breezy pop of Happiness falls into that \u201cshit\u201d category \u2013 they also have a handful of top-tier bops (Obviously, All About You, a raucous One For the Radio), and enough musical variety, to keep even the patient Busted fans happy.</p>"
            },
            "isHosted": False,
            "pillarId": "pillar/arts",
            "pillarName": "Arts",
        },
        {
            "id": "world/2025/sep/18/chinas-temple-economy-in-the-spotlight-as-scandals-rock-influential-religious-leaders",
            "type": "article",
            "sectionId": "world",
            "sectionName": "World news",
            "webPublicationDate": "2025-09-18T02:20:10Z",
            "webTitle": "China\u2019s \u2018temple economy\u2019 in the spotlight as scandals rock influential religious leaders ",
            "webUrl": "https://www.theguardian.com/world/2025/sep/18/chinas-temple-economy-in-the-spotlight-as-scandals-rock-influential-religious-leaders",
            "apiUrl": "https://content.guardianapis.com/world/2025/sep/18/chinas-temple-economy-in-the-spotlight-as-scandals-rock-influential-religious-leaders",
            "fields": {
                "body": '<p>For a religious leader, the allegations were scandalous. Mistresses, illegitimate children, embezzlement. But in 2015, the head abbott of Shaolin monastery, the cradle of Zen Buddhism and kung-fu in China, was untouchable. Shi Yongxin, the so-called \u201cCEO monk\u201d who turned the 1,500-year-old monastery into a commercial empire worth hundreds of millions of yuan, held firm. Soon he was cleared of all charges.</p> <p>But 10 years later, the 60-year-old monk was not so lucky. In July, not long after Shi returned from a trip to the Vatican to meet the late Pope Francis, the Shaolin Temple released a statement saying that <a href="https://www.theguardian.com/world/2025/jul/28/shaolin-temple-abbot-monk-investigation-embezzlement-ntwnfb">he was being investigated</a> for allegedly misappropriating funds and for fathering illegitimate children with multiple mistresses. Less than a fortnight later he was dismissed and stripped of his monkhood. He has not been heard from since.<strong> </strong></p> <p>Shi\u2019s downfall, for accusations similar to those made \u2013 <a href="https://www.theguardian.com/world/2015/aug/02/shaolin-abbot-under-investigation-after-sex-and-claims-surface-online">and survived \u2013 in 2015</a>, was the most high profile in a series of scandals that have rocked China\u2019s Buddhist temples in recent months.</p> '
            },
            "isHosted": False,
            "pillarId": "pillar/news",
            "pillarName": "News",
        },
    ]
