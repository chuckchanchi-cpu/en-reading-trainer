# -*- coding: utf-8 -*-
"""passages.py — 英文閱讀理解題庫（P.6 考試程度）
每篇 passage：5 條 MCQ + 1 條 ONE-word 填詞；每題有 💡提示（定位技巧）+ ⚠️陷阱（干擾項分析）。
skill 類型：detail / not-mentioned / inference / vocabulary / main-idea / cloze
"""

PASSAGES = [
    {
        "id": "robots",
        "title": "Robots in Daily Life",
        "source": "2026-10-16 評估卷 D 部（P.3-P.5）",
        "article": (
            "Robots play an increasingly important role in our daily life. In recent years, scientists have "
            "developed robots in different shapes and forms. Robots that look like cartoon characters are "
            "popular with children. They are now widely used in schools.\n\n"
            "In some schools, robots are used in STEM classes. Their playful and child-friendly qualities make "
            "them popular with students. With the help of robots, students can learn about engineering and "
            "computer science. Some students can build their own robots and control them with computer languages.\n\n"
            "An ice cream shop in Australia has 'hired' some robots to serve customers. The robots can take "
            "orders, scoop ice cream and pour chocolate on top. Customers can also take selfies with the robots, "
            "which makes their experience even more special.\n\n"
            "Robots are also used to do difficult jobs. Some robots can lift heavy objects and join hot metals "
            "together. Some can even help in heart surgery. They are now widely used in construction, industry "
            "and healthcare.\n\n"
            "Robots are becoming smarter. Some lifelike robots can hold simple conversations with people. A "
            "magazine even used a robot to produce an article.\n\n"
            "As robots become smarter, they can do more. Some people believe we will have robot teaching "
            "assistants in schools. They can carry exercise books, teach vocabulary and numbers. But will robots "
            "completely replace teachers? Not likely. Teachers also need to pay attention to every student's "
            "immediate response and provide timely support. This is still a technical challenge."
        ),
        "questions": [
            {
                "type": "mcq", "skill": "detail",
                "q": "Why are robots popular with students in schools?",
                "options": [
                    "They look like cartoon characters.",
                    "They can talk to students.",
                    "They are fun and can help with their learning.",
                    "They can teach students computer languages.",
                ],
                "answer": "They are fun and can help with their learning.",
                "hint": "第二段「playful and child-friendly qualities」＋「help students in STEM classes」→ 有趣同埋幫學習兩個原因一齊答。",
                "trap": "A 只係第一段講玩具層面，唔係學校受歡迎嘅原因；B/D 係部分事實但涵蓋唔到「fun」同「learning」兩點，最完整先係答案。",
            },
            {
                "type": "mcq", "skill": "not-mentioned",
                "q": "Which function of robots is NOT mentioned in the article?",
                "options": [
                    "Join metals together",
                    "Talk to people",
                    "Take photos of customers",
                    "Write articles",
                ],
                "answer": "Take photos of customers",
                "hint": "逆向題：逐項翻原文核對。A→第四段；B→第五段「hold simple conversations」；D→第五段「produce an article」。剩低嗰項就係答案。",
                "trap": "⚠️ 第三段有「take selfies with the robots」，但係顧客自己影相，唔係機械人幫顧客影 — 見到 photos 字眼就揀就中伏！",
            },
            {
                "type": "mcq", "skill": "inference",
                "q": "From the last paragraph, what does the writer think about robots?",
                "options": [
                    "The writer believes robots will soon take over all teaching jobs.",
                    "The writer thinks robots are dangerous and should not be used in the classrooms.",
                    "The writer thinks robots have some limits and cannot fully replace human teachers.",
                    "The writer believes robots can only help teachers with easy tasks.",
                ],
                "answer": "The writer thinks robots have some limits and cannot fully replace human teachers.",
                "hint": "作者觀點睇最後一段結論句：「Not likely」＋「This is still a technical challenge」→ 有局限、唔會完全取代。",
                "trap": "A 同原文「Not likely」相反；D 過度簡化 — 文章冇話「只可以做容易工作」，機械人仲做緊心臟手術等困難工作。",
            },
            {
                "type": "mcq", "skill": "detail",
                "q": "What might customers enjoy about the experience at the ice cream shop with robots?",
                "options": [
                    "Robots are more efficient than human workers.",
                    "Customers can take selfies with the robots, enhancing their experience.",
                    "Robots do not make mistakes when serving ice cream.",
                    "The robots are programmed to tell jokes when serving.",
                ],
                "answer": "Customers can take selfies with the robots, enhancing their experience.",
                "hint": "第三段尾句「take selfies with the robots, which makes their experience even more special」直接對應。",
                "trap": "A/C/D 喺原文完全冇提（efficient、mistakes、jokes 都係自己諗出嚟嘅選項）— 答案要同原文用字對應。",
            },
            {
                "type": "mcq", "skill": "detail",
                "q": "What challenge do teachers face that robots cannot currently address?",
                "options": [
                    "Preparing lesson plans.",
                    "Teaching vocabulary and numbers.",
                    "Responding to each student's immediate needs and providing support.",
                    "Carrying exercise books.",
                ],
                "answer": "Responding to each student's immediate needs and providing support.",
                "hint": "最後一段「teachers also need to pay attention to every student's immediate response and provide timely support. This is still a technical challenge」逐字對應。",
                "trap": "B/D 恰好係機械人做得到嘅嘢（teach vocabulary and numbers、carry exercise books），唔好調轉。",
            },
            {
                "type": "cloze", "skill": "cloze",
                "q": "Complete the sentence with ONE word from the article: With the _____ of robots, students can learn about engineering and computer science.",
                "answer": "help",
                "hint": "常用片語「with the help of」（在……幫助下）；睇前後文：機械人幫學生學習。",
                "trap": "⚠️ 限定 ONE word — 唔可以寫「help of」；亦唔好受中文影響寫「using」（文法通但唔係文中詞語）。",
            },
        ],
    },
    {
        "id": "seaturtle",
        "title": "Sea Turtles in Danger",
        "source": "原創（P.6 考試程度，環保題材）",
        "article": (
            "Sea turtles are large reptiles that have lived in the ocean for millions of years. There are seven "
            "kinds of sea turtles in the world, and some of them are in danger.\n\n"
            "Every year, mother sea turtles swim back to the beach where they were born. They dig holes in the "
            "sand and lay their eggs at night. After about two months, the baby turtles hatch and quickly crawl "
            "towards the sea. Only a few of them will grow up, because many are eaten by birds and crabs.\n\n"
            "Today, sea turtles face more dangers than ever. People throw rubbish into the sea. Sea turtles may "
            "mistake plastic bags for jellyfish and eat them. They may also get caught in fishing nets. Some "
            "people steal their eggs to sell. Because of these problems, the number of sea turtles is dropping "
            "quickly.\n\n"
            "Many people are trying to save sea turtles. Volunteers look after the beaches during the nesting "
            "season. They help baby turtles find their way to the sea and keep them safe from danger. In some "
            "places, people are not allowed to fish near the beaches. Scientists also teach people not to throw "
            "rubbish into the sea.\n\n"
            "Sea turtles have lived on Earth longer than dinosaurs. If we do not help them, these amazing "
            "animals may disappear forever."
        ),
        "questions": [
            {
                "type": "mcq", "skill": "detail",
                "q": "Why do mother sea turtles swim back to the same beach every year?",
                "options": [
                    "To find food.",
                    "To lay eggs.",
                    "To escape from danger.",
                    "To meet other sea turtles.",
                ],
                "answer": "To lay eggs.",
                "hint": "第二段開頭：「swim back to the beach where they were born」跟住「dig holes... and lay their eggs」→ 返嚟係為咗產卵。",
                "trap": "A 係常識式干擾（以為返海灘搵嘢食），但原文完全冇提搵食物 — 答案要跟原文。",
            },
            {
                "type": "mcq", "skill": "not-mentioned",
                "q": "Which of the following is NOT mentioned as a danger to sea turtles in the article?",
                "options": [
                    "Plastic bags in the sea.",
                    "Fishing nets.",
                    "Rising sea levels.",
                    "People stealing their eggs.",
                ],
                "answer": "Rising sea levels.",
                "hint": "第三段逐項核對：plastic bags ✓、fishing nets ✓、steal their eggs ✓ — 剩低嗰項文中冇提。",
                "trap": "⚠️ Rising sea levels 喺環保新聞成日見，好似好合理 — 但「合理」唔等於「有提」，逆向題只信原文。",
            },
            {
                "type": "mcq", "skill": "vocabulary",
                "q": "The sea turtles may 'mistake plastic bags for jellyfish' in paragraph 3. What does this mean?",
                "options": [
                    "They think plastic bags are jellyfish by accident.",
                    "They like jellyfish more than plastic bags.",
                    "They see plastic bags and swim away.",
                    "They eat jellyfish beside the plastic bags.",
                ],
                "answer": "They think plastic bags are jellyfish by accident.",
                "hint": "「mistake A for B」= 誤認 A 係 B。跟住「and eat them」→ 認錯咗先至食落肚。",
                "trap": "B 用「more than」做比較，原文冇比較喜好；C/D 係自己幻想出嚟嘅情節。片語題要整句解，唔係逐字譯。",
            },
            {
                "type": "mcq", "skill": "inference",
                "q": "From paragraph 2, what can we learn about baby turtles?",
                "options": [
                    "They grow up very slowly with their mother.",
                    "Most of them will not grow up.",
                    "Mother turtles lay only a few eggs.",
                    "They hatch during the daytime.",
                ],
                "answer": "Most of them will not grow up.",
                "hint": "「Only a few of them will grow up」→ 反過來即係大多數長唔大。推論題用「反面理解」技巧。",
                "trap": "A 中伏位：海龜媽媽生完蛋就離開，幼龜唔係跟媽媽長大；D 調轉 — 原文話夜晚產卵，幼龜約兩個月後孵出，冇講日間。",
            },
            {
                "type": "mcq", "skill": "main-idea",
                "q": "What is the main idea of paragraph 4?",
                "options": [
                    "Volunteers enjoy looking after beaches.",
                    "People are trying to save sea turtles.",
                    "People are not allowed to fish near beaches.",
                    "Scientists teach people about rubbish.",
                ],
                "answer": "People are trying to save sea turtles.",
                "hint": "段旨睇第一句（topic sentence）：「Many people are trying to save sea turtles」，後面嘅例子都係支撐呢句。",
                "trap": "A/C/D 都係段入面嘅「例子」，只係部分內容 — 主旨題要揀覆蓋全段嘅答案，唔好揀例子。",
            },
            {
                "type": "cloze", "skill": "cloze",
                "q": "Complete the sentence with ONE word from the article: Volunteers help baby turtles find their way to the sea and keep them _____ from danger.",
                "answer": "safe",
                "hint": "常用句式「keep + 人/物 + 形容詞」（keep them safe）；睇前文：義工保護幼龜。",
                "trap": "⚠️ 唔好寫「safely」— keep 後面用形容詞做補語（keep them safe ✅ / keep them safely ❌）；亦要係文中詞語。",
            },
        ],
    },
    {
        "id": "breakfast",
        "title": "Why Breakfast Matters",
        "source": "原創（P.6 考試程度，健康題材）",
        "article": (
            "Many people are too busy to eat breakfast. Some say they want to sleep a little longer. Some say "
            "they are not hungry in the morning. However, doctors say that breakfast is the most important meal "
            "of the day.\n\n"
            "After a long night, our body needs energy to start a new day. Breakfast gives us the energy to "
            "think and to move. Studies show that students who eat breakfast get better marks in tests. They can "
            "also pay more attention in class. If you skip breakfast, you may feel tired and find it hard to "
            "concentrate.\n\n"
            "A good breakfast should be balanced. It should include some grain foods such as bread or rice. "
            "Milk, eggs and meat give us protein, which helps us grow. Fruit and vegetables give us vitamins. A "
            "bowl of noodles with an egg and an orange is a good example.\n\n"
            "Some people eat breakfast but choose the wrong food. Sweet biscuits and soft drinks have a lot of "
            "sugar. They give energy for a short time only. Soon after, you will feel tired again. It is better "
            "to choose healthy food.\n\n"
            "If you want to stay healthy and study well, never skip breakfast. Eat a balanced breakfast every "
            "morning, and you will have a great start to your day."
        ),
        "questions": [
            {
                "type": "mcq", "skill": "detail",
                "q": "According to the article, students who eat breakfast can _____.",
                "options": [
                    "sleep longer",
                    "pay more attention in class",
                    "grow much taller than others",
                    "get more vitamins from milk",
                ],
                "answer": "pay more attention in class",
                "hint": "第二段「Studies show that students who eat breakfast... They can also pay more attention in class」直接對應。",
                "trap": "C 過度推論 — protein 幫生長，但原文冇話食早餐會「長高啲」；答案要原文直接支援。",
            },
            {
                "type": "mcq", "skill": "not-mentioned",
                "q": "Which of the following is NOT mentioned as part of a good breakfast?",
                "options": [
                    "Bread",
                    "Milk",
                    "Sweet biscuits",
                    "Fruit",
                ],
                "answer": "Sweet biscuits",
                "hint": "第三段列舉好早餐：grain foods（bread/rice）✓、milk/eggs/meat ✓、fruit/vegetables ✓。Sweet biscuits 喺第四段出現，但係「wrong food」。",
                "trap": "⚠️ Sweet biscuits 喺原文見得到 — 但佢係「反面教材」，唔係好早餐一部分。見到字眼就揀、冇理佢喺邊段出現，就係呢條陷阱設計。",
            },
            {
                "type": "mcq", "skill": "inference",
                "q": "Why do sweet biscuits and soft drinks give energy for a short time only?",
                "options": [
                    "They have a lot of sugar.",
                    "They are not delicious.",
                    "People eat too little of them.",
                    "They have no vitamins at all.",
                ],
                "answer": "They have a lot of sugar.",
                "hint": "第四段：「Sweet biscuits and soft drinks have a lot of sugar. They give energy for a short time only.」前句就係原因。",
                "trap": "B/D 原文冇講（冇提好唔好味，亦冇話完全冇維他命）— 推論要基於原文線索，唔係靠常識亂諗。",
            },
            {
                "type": "mcq", "skill": "vocabulary",
                "q": "What does 'skip breakfast' in paragraph 2 mean?",
                "options": [
                    "Eat breakfast late.",
                    "Not eat breakfast.",
                    "Eat breakfast very quickly.",
                    "Buy breakfast outside.",
                ],
                "answer": "Not eat breakfast.",
                "hint": "由上下文推：「If you skip breakfast, you may feel tired and find it hard to concentrate」→ 唔食早餐先會有呢啲後果。",
                "trap": "A/C 都係「有食但遲/快」— skip 係「跳過、唔做」，唔係快慢問題。詞義題要靠後果反推。",
            },
            {
                "type": "mcq", "skill": "main-idea",
                "q": "What is the article mainly about?",
                "options": [
                    "How to make a balanced breakfast.",
                    "Why breakfast is important and what we should eat.",
                    "Why some students get better marks in tests.",
                    "Sweet food and soft drinks are bad for us.",
                ],
                "answer": "Why breakfast is important and what we should eat.",
                "hint": "主旨題要覆蓋全文：第一、二段講「點解重要」，第三、四段講「食咩好」— 兩部分都要包。",
                "trap": "A/C/D 各自只覆蓋一部分（A→第三段、C→第二段、D→第四段），太窄唔可以做主旨。",
            },
            {
                "type": "cloze", "skill": "cloze",
                "q": "Complete the sentence with ONE word from the article: A good breakfast should be _____. It should include some grain foods such as bread or rice.",
                "answer": "balanced",
                "hint": "後句話要「include」唔同種類食物（穀物、蛋白質、蔬果）→ 即係「均衡」。呢個字喺第三段第一句。",
                "trap": "⚠️ 好多人寫「delicious」（好味）— 但文章講營養均衡，唔係講味道；ONE word 限定，亦唔可以寫「good for you」。",
            },
        ],
    },
    {
        "id": "solar",
        "title": "Solar Energy — Power from the Sun",
        "source": "原創（P.6 考試程度，科技/環保題材）",
        "article": (
            "The sun is a great source of energy. Every day, it sends a huge amount of heat and light to the "
            "Earth. People can change sunlight into electricity by using solar panels. This kind of electricity "
            "is called solar energy.\n\n"
            "Solar energy is clean. It does not produce smoke or dirty gases. Unlike coal and oil, the sun will "
            "not run out for billions of years. More and more families in Hong Kong put solar panels on the "
            "roofs of their houses. They use solar energy to heat water and to power lights.\n\n"
            "Solar energy is also used in many other ways. Some villages without electricity use solar panels to "
            "get power. Farmers use solar energy to pump water for their crops. Scientists even put solar panels "
            "on satellites and space stations.\n\n"
            "However, solar energy is not perfect. Solar panels cannot work at night or on very rainy days. They "
            "also cost a lot of money to buy and to put up. Scientists are working hard to make solar panels "
            "cheaper and better.\n\n"
            "One day, solar energy may become our main source of power. If we use more of it, the Earth will be "
            "a cleaner and greener place."
        ),
        "questions": [
            {
                "type": "mcq", "skill": "detail",
                "q": "How do people change sunlight into electricity?",
                "options": [
                    "By burning coal and oil.",
                    "By using solar panels.",
                    "By heating water on the roofs.",
                    "By putting panels under the sea.",
                ],
                "answer": "By using solar panels.",
                "hint": "第一段：「People can change sunlight into electricity by using solar panels」逐字對應。",
                "trap": "A 係另一種發電方法（原文用嚟對比）；C 係第二段嘅「用途」，唔係轉換方法。",
            },
            {
                "type": "mcq", "skill": "not-mentioned",
                "q": "Which of the following is NOT mentioned as a use of solar energy?",
                "options": [
                    "Heating water.",
                    "Pumping water for crops.",
                    "Cooking food.",
                    "Powering satellites.",
                ],
                "answer": "Cooking food.",
                "hint": "第二、三段核對：heat water ✓（第二段）、pump water for crops ✓（第三段）、satellites ✓（第三段）— 剩低 cooking food 冇提。",
                "trap": "⚠️「太陽能煮嘢」好似好合理（太陽能爐真係存在），但逆向題只計原文有冇提，唔計常識上可唔可能。",
            },
            {
                "type": "mcq", "skill": "inference",
                "q": "Why do scientists put solar panels on satellites and space stations?",
                "options": [
                    "To make the satellites look modern.",
                    "Because satellites need power and there is plenty of sunlight in space.",
                    "Because satellites are very expensive.",
                    "To heat water for astronauts.",
                ],
                "answer": "Because satellites need power and there is plenty of sunlight in space.",
                "hint": "推論題：第三段列舉用途（villages→get power、farmers→pump water），同樣道理 — 衛星需要電力，而太空有充足陽光。",
                "trap": "A/C 原文冇提（modern、expensive 衛星）；D 係張冠李戴（heat water 係第二段地面家庭嘅用途）。",
            },
            {
                "type": "mcq", "skill": "vocabulary",
                "q": "What does 'run out' in paragraph 2 mean?",
                "options": [
                    "Run very quickly.",
                    "Be used up.",
                    "Become expensive.",
                    "Become dirty.",
                ],
                "answer": "Be used up.",
                "hint": "前後文對比：「Unlike coal and oil, the sun will not run out for billions of years」→ 煤同石油會用盡，太陽唔會。",
                "trap": "A 逐字譯「跑」— 片語動詞要按上下文解，唔係逐個字翻譯。",
            },
            {
                "type": "mcq", "skill": "detail",
                "q": "Which problem of solar panels is mentioned in paragraph 4?",
                "options": [
                    "They produce smoke and dirty gases.",
                    "They cost a lot of money.",
                    "They cannot work on sunny days.",
                    "They are difficult to put on roofs.",
                ],
                "answer": "They cost a lot of money.",
                "hint": "第四段：「They also cost a lot of money to buy and to put up」→ 花費高係講明嘅問題。",
                "trap": "A 倒果為因（唔產氣係第二段講嘅「好處」）；C 轉咗彎 — 係夜晚同雨天唔得，唔係晴天；D 偷換概念（put up 係安裝，冇話「難」）。",
            },
            {
                "type": "cloze", "skill": "cloze",
                "q": "Complete the sentence with ONE word from the article: Solar energy is clean. It does not produce smoke or dirty _____.",
                "answer": "gases",
                "hint": "同「smoke」並列嘅名詞，指工廠/車輛排出嘅污濁氣體；呢個字喺第二段第二句。",
                "trap": "⚠️ 注意單複數 — 原文用複數「gases」（dirty gases）；寫「gas」文法上勉強通但唔係原文詞語，ONE word 題要跟原文。",
            },
        ],
    },
]
