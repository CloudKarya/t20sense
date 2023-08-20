import requests, os, pickle
import pandas as pd
from google.cloud import storage  # Google Cloud Storage Imports

# Set the path to your service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 't20-sense-8f218a81848c.json'

# Create a client using the credentials
storage_client = storage.Client()

ipl_player_dictionary = {80607: 'Tushar Deshpande', 58403: 'Devon Conway', 95094: 'Ruturaj Gaikwad', 46597: 'Moeen Ali', 53320: 'Ben Stokes', 8999: 'Ambati Rayudu', 74975: 'Shivam Dube', 49247: 'Ravindra Jadeja', 7593: 'MS Dhoni', 64864: 'Mitchell Santner', 62022: 'Deepak Chahar', 104758: 'Rajvardhan Hangargekar', 51088: 'Kane Williamson', 51216: 'Wriddhiman Saha', 95316: 'Shubman Gill', 102753: 'Sai Sudharsan', 70633: 'Hardik Pandya', 63509: 'Vijay Shankar', 60628: 'Rahul Tewatia', 79159: 'Rashid Khan', 63646: 'Mohammed Shami', 85975: 'Josh Little', 103597: 'Yash Dayal', 72397: 'Alzarri Joseph', 51491: 'Rishi Dhawan', 103766: 'Prabhsimran Singh', 15887: 'Shikhar Dhawan', 56511: 'Bhanuka Rajapaksa', 75347: 'Jitesh Sharma', 52319: 'Sikandar Raza', 72103: 'Sam Curran', 75315: 'M Shahrukh Khan', 104281: 'Harpreet Brar', 95219: 'Rahul Chahar', 101430: 'Arshdeep Singh', 80817: 'Nathan Ellis', 98673: 'Varun Chakravarthy', 59601: 'Mandeep Singh', 90143: 'Rahmanullah Gurbaz', 96408: 'Anukul Roy', 81147: 'Venkatesh Iyer', 70411: 'Nitish Rana', 75591: 'Rinku Singh', 51012: 'Andre Russell', 63477: 'Shardul Thakur', 49039: 'Sunil Narine', 49108: 'Tim Southee', 58274: 'Umesh Yadav', 60530: 'KL Rahul', 56832: 'Kyle Mayers', 64479: 'Deepak Hooda', 63224: 'Krunal Pandya', 54212: 'Marcus Stoinis', 70405: 'Nicholas Pooran', 102735: 'Ayush Badoni', 60737: 'Krishnappa Gowtham', 73507: 'Avesh Khan', 104770: 'Ravi Bishnoi', 59261: 'Jaydev Unadkat', 56993: 'Mark Wood', 87603: 'Khaleel Ahmed', 95315: 'Prithvi Shaw', 48739: 'David Warner', 50771: 'Mitchell Marsh', 71335: 'Sarfaraz Khan', 53649: 'Rilee Rossouw', 80425: 'Rovman Powell', 108718: 'Aman Hakim Khan', 67455: 'Axar Patel', 67609: 'Kuldeep Yadav', 101780: 'Chetan Sakariya', 85763: 'Mukesh Kumar', 74633: 'Navdeep Saini', 102743: 'Yashasvi Jaiswal', 53271: 'Jos Buttler', 60806: 'Sanju Samson', 100878: 'Devdutt Padikkal', 96392: 'Riyan Parag', 72393: 'Shimron Hetmyer', 12894: 'Ravichandran Ashwin', 59339: 'Jason Holder', 51092: 'Trent Boult', 96757: 'KM Asif', 61325: 'Yuzvendra Chahal', 90231: 'Fazalhaq Farooqi', 95320: 'Abhishek Sharma', 59599: 'Mayank Agarwal', 61999: 'Rahul Tripathi', 84027: 'Harry Brook', 75311: 'Washington Sundar', 80639: 'Glenn Phillips', 104814: 'Abdul Samad', 49427: 'Adil Rashid', 54282: 'Bhuvneshwar Kumar', 108529: 'Umran Malik', 79597: 'T Natarajan', 50789: 'Jason Behrendorff', 48405: 'Rohit Sharma', 75325: 'Ishan Kishan', 96335: 'Cameron Green', 61990: 'Suryakumar Yadav', 104396: 'Tilak Varma', 102738: 'Nehal Wadhera', 83439: 'Tim David', 104752: 'Hrithik Shokeen', 108342: 'Arshad Khan', 47185: 'Piyush Chawla', 72379: 'Jofra Archer', 49752: 'Virat Kohli', 46933: 'Faf du Plessis', 8813: 'Dinesh Karthik', 54222: 'Glenn Maxwell', 54369: 'Michael Bracewell', 103588: 'Shahbaz Ahmed', 59260: 'Harshal Patel', 104922: 'Akash Deep', 62587: 'Reece Topley', 87477: 'Mohammed Siraj', 15731: 'Karn Sharma', 95329: 'Yash Thakur', 110107: 'Abishek Porel', 63651: 'Anrich Nortje', 53891: 'David Miller', 104817: 'Dhruv Jurel', 114312: 'Suyash Sharma', 101312: 'Anuj Rawat', 53121: 'David Willey', 81141: 'Anmolpreet Singh', 70277: 'Aiden Markram', 12562: 'Amit Mishra', 72505: 'Romario Shepherd', 66116: 'Murugan Ashwin', 61797: 'Sandeep Sharma', 51454: 'Manish Pandey', 86109: 'Lalit Yadav', 103701: 'Kumar Kartikeya', 69697: 'Tristan Stubbs', 51096: 'Ajinkya Rahane', 54430: 'Dwaine Pretorius', 58466: 'Sisanda Magala', 77887: 'Abhinav Manohar', 94125: 'Narayan Jagadeesan', 64402: 'Lockie Ferguson', 70472: 'Matthew Short', 114254: 'Mohit Rathee', 61634: 'Heinrich Klaasen', 73871: 'Marco Jansen', 96617: 'Mayank Markande', 81197: 'Mahipal Lomror', 50121: 'Wayne Parnell', 110977: 'Yash Dhull', 54674: 'Mustafizur Rahman', 89779: 'Riley Meredith', 58435: 'Adam Zampa', 104045: 'Kuldeep Sen', 101991: 'Maheesh Theekshana', 104787: 'Akash Singh', 67296: 'Kagiso Rabada', 66722: 'Mohit Sharma', 78239: 'Wanindu Hasaranga', 77873: 'Vijaykumar Vyshak', 106850: 'Yudhvir Singh', 101424: 'Atharva Taide', 56442: 'Harpreet Singh', 102574: 'Arjun Tendulkar', 69674: 'Duan Jansen', 105215: 'Noor Ahmad', 105938: 'Matheesha Pathirana', 96803: 'Suyash Prabhudessai', 79151: 'Naveen-ul-Haq', 59832: 'Liam Livingstone', 52290: 'Jason Roy', 66691: 'Litton Das', 96758: 'Kulwant Khejroliya', 49327: 'Ishant Sharma', 72363: 'Phil Salt', 87569: 'Mayank Dagar', 62051: 'Jayant Yadav', 88977: 'Prerak Mankad', 110638: 'Abdul Basith', 48777: 'David Wiese', 106418: 'Ripal Patel', 107007: 'Vaibhav Arora', 106886: 'Kuldip Yadav', 110604: 'Gurnoor Brar', 111976: 'Harshit Rana', 66259: 'Akeal Hosein', 95319: 'Priyam Garg', 51367: 'Josh Hazlewood', 66358: 'Manan Vohra', 108519: 'Karan Sharma', 101792: 'Mohsin Khan', 106837: 'Akash Madhwal', 101306: 'Kartik Tyagi', 114297: 'Raghav Goyal', 51482: 'Kedar Jadhav', 58406: 'Quinton de Kock', 49096: 'Swapnil Singh', 83915: 'Obed McCoy', 52656: 'Joe Root', 108645: 'Vivrant Sharma', 51421: 'Chris Jordan', 75995: 'Vishnu Vinod', 77821: 'Praveen Dubey', 61690: 'Dasun Shanaka', 101804: 'Sanvir Singh', 104825: 'Nitish Kumar Reddy', 114290: 'Himanshu Sharma', 99252: 'Darshan Nalkande', 8742: 'Robin Uthappa', 45257: 'Dwayne Bravo', 62153: 'Adam Milne', 71331: 'Shreyas Iyer', 52241: 'Sam Billings', 49357: 'Sheldon Jackson', 96417: 'Shivam Mavi', 49040: 'Kieron Pollard', 80807: 'Daniel Sams', 62490: 'Tymal Mills', 70640: 'Jasprit Bumrah', 75993: 'Basil Thampi', 70695: 'Tim Seifert', 86165: 'Rishabh Pant', 95323: 'Kamlesh Nagarkoti', 84201: 'Sherfane Rutherford', 110981: 'Raj\xa0Bawa', 80451: 'Odean Smith', 61413: 'Evin Lewis', 67342: 'Dushmantha Chameera', 49024: 'Matthew Wade', 57444: 'Varun Aaron', 49958: 'Nathan Coulter-Nile', 84635: 'Prasidh Krishna', 101414: 'Mukesh Choudhary', 62500: 'Andrew Tye', 95429: 'Dewald Brevis', 64244: 'Pat Cummins', 103872: 'Rasikh Salam', 52161: 'Jonny Bairstow', 58341: 'Shashank Singh', 96395: 'Ramandeep Singh', 55398: 'Rassie van der Dussen', 57196: 'James Neesham', 35812: 'Aaron Finch', 66101: 'Jagadeesha Suchith', 72385: 'Fabian Allen', 59600: 'Karun Nair', 58772: 'Daryl Mitchell', 80645: 'Rajat Patidar', 63522: 'Baba Indrajith', 51181: 'Pradeep Sangwan', 103599: 'Simarjeet Singh', 59610: 'Sean Abbott', 56596: 'Shreyas Gopal', 66183: 'Srikar Bharat', 94051: 'Sai Kishore', 108612: 'Prashant Solanki', 94153: 'Sanjay Yadav', 96532: 'Abhijeet Tomar', 54283: 'Siddarth Kaul', 54340: 'Chris Lynn', 46533: 'AB de Villiers', 44853: 'Dan Christian', 70691: 'Kyle Jamieson', 15716: 'Suresh Raina', 49496: 'Chris Woakes', 67312: 'Tom Curran', 47055: 'Eoin Morgan', 48277: 'Shakib Al Hasan', 7139: 'Harbhajan Singh', 46888: 'Mohammad Nabi', 7568: 'Chris Gayle', 77669: 'Jhye Richardson', 61832: 'Chris Morris', 15308: 'Shahbaz Nadeem', 75321: 'Virat Singh', 90165: 'Mujeeb Ur Rahman', 49346: 'Jalaj Saxena', 50281: 'Steven Smith', 68063: 'Lukman Meriwala', 47078: 'Moises Henriques', 66941: 'Lungi Ngidi', 50709: 'Kane Richardson', 19422: 'Imran Tahir', 51098: 'Dhawal Kulkarni', 49309: 'Dawid Malan', 15317: 'Saurabh Tiwary', 61479: 'Sachin Baby', 89889: 'Ishan Porel', 58408: 'Tabraiz Shamsi', 69227: 'Sandeep Warrier', 71379: 'George Garton', 50781: 'James Pattinson', 49342: 'Murali Vijay', 10125: 'Shane Watson', 64443: 'Sheldon Cottrell', 101339: 'Josh Philippe', 47154: 'Dale Steyn', 67458: 'Nikhil Naik', 69114: 'Ankit Rajpoot', 66725: 'Gurkeerat Singh Mann', 54460: 'Isuru Udana', 54314: 'Alex Carey', 82071: 'Tom Banton', 78281: 'Chris Green', 73505: 'Monu Kumar', 52539: 'Shreevats Goswami', 9900: 'Parthiv Patel', 47231: 'Colin de Grandhomme', 15473: 'Yusuf Pathan', 48155: 'Colin Ingram', 72509: 'Keemo Paul', 7716: 'Yuvraj Singh', 49028: 'Ben Cutting', 53716: 'Mitchell McClenaghan', 58253: 'Hardus Viljoen', 45105: 'Lasith Malinga', 62182: 'Hanuma Vihari', 89165: 'Sandeep Lamichhane', 103589: 'Prayas Ray Barman', 64767: 'Akshdeep Nath', 10553: 'Stuart Binny', 66253: 'Pawan Negi', 66844: 'Scott Kuggeleijn', 64741: 'Prashant Chopra', 101751: 'Sudhesan Midhun', 49441: 'Harry Gurney', 60557: 'Siddhesh Lad', 46925: 'Joe Denly', 62457: 'Carlos Brathwaite', 49106: 'Colin Munro', 71341: 'Ricky Bhui', 64758: 'Ashton Turner', 67586: 'Ish Sodhi', 101217: 'Prithvi Raj', 77835: 'KC Cariappa', 84225: 'Oshane Thomas', 68885: 'Dhruv Shorey', 66726: 'Barinder Sran', 48927: 'Martin Guptill', 7773: 'Gautam Gambhir', 10384: 'Brendon McCullum', 10556: 'Vinay Kumar', 10130: 'Mitchell Johnson', 53268: "D'Arcy Short", 53439: 'Ben Laughlin', 66371: 'Billy Stanlake', 68065: 'Akila Dananjaya', 51057: 'Corey Anderson', 45443: 'Liam Plunkett', 47624: 'Manoj Tiwary', 45222: 'Jean-Paul Duminy', 49532: 'Alex Hales', 12701: 'Naman Ojha', 58299: 'Anureet Singh', 60609: 'Ankit Sharma', 49035: 'Javon Searles', 67090: 'Junior Dala', 47347: 'Bipul Sharma', 7804: 'Ashish Nehra', 66190: 'Travis Head', 51455: 'Sreenath Aravind', 66085: 'Aniket Choudhary', 7520: 'Rajat Bhatia', 48965: 'Ashok Dinda', 45554: 'Dwayne Smith', 53549: 'Manpreet Gony', 48319: 'Praveen Kumar', 7458: 'Shadab Jakati', 84649: 'Shivil Kaushik', 9952: 'Hashim Amla', 51050: 'Iqbal Abdulla', 55296: 'Aditya Tare', 7678: 'Zaheer Khan', 96752: 'Tejas Baroka', 45772: 'Samuel Badree', 47100: 'Munaf Patel', 47023: 'Angelo Mathews', 10129: 'Shaun Marsh', 50483: 'James Faulkner', 96401: 'Shubham Agarwal', 81195: 'Nathu Singh', 53314: 'Abhimanyu Mithun', 56438: 'Eklavya Dwivedi', 68573: 'Pravin Tambe', 78923: 'Tanmay Agarwal', 51054: 'Darren Bravo', 96768: 'Ankit Soni', 54385: 'Ankit Bawne', 11399: 'Irfan Pathan', 10238: 'Marlon Samuels', 45256: 'Lendl Simmons', 64947: 'Matt Henry', 51189: 'Ishank Jaggi', 8107: 'Kevin Pietersen', 47123: 'RP Singh', 49002: 'John Hastings', 3328: 'Brad Hogg', 46717: 'Pardeep Sahu', 53548: 'Sarabjit Ladda', 58365: 'Parvez Rasool', 59215: 'Ashish Reddy', 47289: 'Morne Morkel', 49193: 'Thisara Perera', 52222: 'Kyle Abbott', 9505: 'Albie Morkel', 7519: 'Rajagopal Sathish', 55321: 'Peter Handscomb', 61993: 'Scott Boland', 48671: 'Usman Khawaja', 35384: 'George Bailey', 48148: 'Farhaan Behardien', 61988: 'Unmukt Chand', 48431: 'Pragyan Ojha', 62033: 'Ishwar Pandey', 52521: 'Chidhambaram Gautam', 66143: 'Domnic Muthuswami', 7781: 'Virender Sehwag', 53978: 'Karanveer Singh', 44691: 'Ravi Bopara', 44829: 'Daren Sammy', 48998: 'Abu Nechim', 61383: 'Pawan Suyal', 45358: 'Ryan ten Doeschate', 11920: 'Manvinder  Bisla', 75249: 'Shivam Sharma', 10401: 'Johan Botha', 53330: 'Mitchell Starc', 4173: 'Azhar Mahmood', 44876: 'Sumit Narwal', 66142: 'Veer Pratap Singh', 68883: 'Vaibhav Rawal', 75799: 'Aditya Garhwal', 8726: 'Dishant Yagnik', 46695: 'Vikramjeet Malik', 47308: 'Abhishek Nayar', 48863: 'Rusty Theron', 51109: 'Dinesh Salunkhe', 81273: 'Sagar Trivedi', 60691: 'Ronit More', 64707: 'Gurinder Sandhu', 55245: 'Nic Maddinson', 59394: 'Marchant de Lange', 58511: 'Beuran Hendricks', 6256: 'Michael Hussey', 2232: 'Jacques Kallis', 44930: 'Ross Taylor', 50810: 'Rahul Sharma', 47340: 'Sachin Rana', 17752: 'Cheteshwar Pujara', 54010: 'Parvinder Awana', 9022: 'Lakshmipathy Balaji', 8163: 'Venugopal Rao', 6253: 'Brad Hodge', 7136: 'Murali Kartik', 7630: 'Mithun Manhas', 44865: 'Ben Hilfenhaus', 12928: 'Yogesh Takawale', 2041: 'Muthiah Muralidaran', 7704: 'Laxmi Shukla', 45258: 'Ravi Rampaul', 59118: 'Ben Dunk', 59266: 'Rahul Shukla', 67457: 'Vijay Zol', 58185: 'Kevon Cooper', 11984: 'David Hussey', 53391: 'Krishmar Santokie', 8814: 'Srikkanth Anirudha', 6315: 'Mahela Jayawardene', 59259: 'Manprit Juneja', 5966: 'Brett Lee', 7419: 'Tillakaratne Dilshan', 53754: 'Arun Karthik', 2230: 'Ricky Ponting', 1934: 'Sachin Tendulkar', 9989: 'Jacob Oram', 58269: 'Akshath Reddy', 9587: 'Kumar Sangakkara', 12049: 'Cameron White', 49361: 'Dwaraka Ravi Teja', 52373: 'Kusal Perera', 2281: 'Rahul Dravid', 58116: 'Ashok Menaria', 12020: 'Sreesanth', 9815: 'Siddharth Trivedi', 8821: 'S Badrinath', 47695: 'Dirk Nannes', 12084: 'Tirumalasetti Suman', 4176: 'Adam Gilchrist', 12601: 'Ryan Harris', 17780: 'Shaun Tait', 61318: 'Biplab Samantray', 24777: 'Jeevan Mendis', 45890: 'Ryan McLaren', 60588: 'Harmeet Singh', 48381: 'Anand Rajan', 44814: 'Jamaluddin Syed Mohammad', 50837: 'Sachithra Senanayake', 47324: 'Ajit  Chandila', 54479: 'Debabrata Das', 47079: 'Ben Rohrer', 9253: 'Andrew McDonald', 55401: 'Ankeet Chavan', 7129: 'Ajit Agarkar', 7793: 'Paul Valthaty', 6769: 'Dimitri Mascarenhas', 47391: 'Roelof van der Merwe', 44660: 'Luke Wright', 50377: 'Ajantha Mendis', 15732: 'Ali Murtaza', 49092: 'Luke Pomersbach', 59325: 'Harmeet Singh', 61489: 'Bhargav Bhatt', 53753: 'Thalaivan Sargunam', 52541: 'Abhinav Mukund', 6377: 'Owais Shah', 47252: 'Mahesh Rawat', 50068: 'Udit Birla', 61411: 'Krishnakant  Upadhyay', 58276: 'Michael Neser', 8807: 'Raiphi Gomez', 12018: 'Bharat Chipli', 12619: 'Paras Dogra', 45487: 'Doug Bollinger', 48359: 'Richard Levi', 9639: 'James Franklin', 53582: 'Yogesh Nagar', 2024: 'Sourav Ganguly', 26889: 'Callum Ferguson', 48269: 'Amit Singh', 4380: 'Daniel Vettori', 57609: 'Doug Bracewell', 9707: 'Daniel Harris', 10145: 'TP Sudhindra', 44946: 'Jesse Ryder', 17731: 'Raju Bhatkal', 46206: 'Nuwan Kulasekara', 48373: 'Yo Mahesh', 48249: 'Pankaj Singh', 7632: 'Mohammad Kaif', 35344: 'Davy Jacobs', 47693: 'Clint McKay', 48189: 'Tanmay Mishra', 8021: 'Abhishek Jhunjhunwala', 50409: 'KP Appanna', 50884: 'Nitin Saini', 10562: 'Alfonso Thomas', 55402: 'Siddharth Chitnis', 6426: 'Brad Haddin', 54391: 'Iresh Saxena', 66087: 'Chirag Jani', 7634: 'Arjun Yadav', 8998: 'Syed Quadri', 15739: 'Tanmay Srivastava', 49005: 'Sunny Sohal', 56407: 'Tekkami Atchuta Rao', 56415: 'Kedar Devdhar', 61985: 'Akash Bhandari', 66001: 'Sneha Kishore', 9492: 'Robin Peterson', 47065: 'Aiden Blizzard', 8876: 'Michael Clarke', 61334: 'Asad Pathan', 51196: 'Prasanth Parameswaran', 48248: 'Anustup Majumdar', 10671: 'Ramesh Powar', 8539: 'Mohnish  Mishra', 2347: 'Herschelle Gibbs', 50618: 'Sunny Gupta', 9570: 'Scott Styris', 11385: 'Suraj Randiv', 54137: 'Amit Paunikar', 49042: 'Abhishek Raut', 2000: 'Shane Warne', 3317: 'VVS Laxman', 47186: 'Sunny Singh', 15813: 'Nathan Rimmington', 10406: 'Graeme Smith', 51187: 'Shrikant Wagh', 4130: 'Johan van der Wath', 57148: 'Ryan Ninan', 36039: 'Nayan Doshi', 4382: 'Andrew Symonds', 9235: 'James Hopes', 9982: 'Faiz Fazal', 7540: 'Charl Langeveldt', 51346: 'Jonathan Vandiar', 54131: 'Nuwan Pradeep', 60529: 'Abrar Kazi', 12106: 'Swapnil Asnodkar', 48349: 'Pinal Shah', 49314: 'Aditya Dole', 53571: 'Samad Fallah', 34747: 'Tim Paine', 45592: 'Joginder Sharma', 8161: 'Shalabh Srivastava', 10386: 'Nathan McCullum', 46591: 'Jerome Taylor', 12036: 'Travis Birt', 59324: 'Kamran Khan', 8241: 'Michael Klinger', 7987: 'Balachandra Akhil', 3947: 'Mark Boucher', 11830: 'Ishan Malhotra', 11930: 'Aavishkar Salvi', 48263: 'Love Ablish', 10787: 'Michael Lumb', 7575: 'Sridharan Sriram', 21588: 'Padmanabhan Prasanth', 8989: 'Gnaneswara Rao', 51220: 'Shrikant Mundhe', 7432: 'Ray Price', 7642: 'Anirudh Singh', 2166: 'Chaminda Vaas', 58265: 'Jaskaran Singh', 1988: 'Sanath Jayasuriya', 10485: 'Amit Uniyal', 48879: 'Yusuf Abdulla', 11374: 'Farveez Maharoof', 1973: 'Anil Kumble', 7133: 'Rohan Gavaskar', 2119: 'Matthew Hayden', 6335: 'Justin Kemp', 53581: 'Sudeep Tyagi', 10280: 'Shane Bond', 2066: 'Damien Martyn', 50886: 'Adrian Barath', 12400: 'Adam Voges', 15851: 'Karan Goel', 15267: 'Thilan Thushara', 49034: 'Kemar Roach', 2314: 'Paul Collingwood', 9946: 'Chandrasekar Ganapathy', 49403: 'Mohnish Parmar', 9925: 'Azhar Bilakhia', 7128: 'Reetinder Sodhi', 49750: 'Bodapati Sumanth', 12548: 'Chandan Madan', 11271: 'Dilhara Fernando', 47184: 'Vikram Singh', 51479: 'Rohan Raje', 4271: 'Andrew Flintoff', 7708: 'Niraj Patel', 7549: 'Tyron Henderson', 54936: 'Taruwar Kohli', 7786: 'Aakash Chopra', 45774: 'Fidel Edwards', 49318: 'Rajesh Bishnoi', 45617: 'Yashpal Singh', 9891: 'Jaydev Shah', 10303: 'Kyle Mills', 17850: 'Luke Ronchi', 24667: 'Mohammad Ashraful', 48253: 'Chetanya Nanda', 51158: 'Rahil Shaikh', 2071: 'Justin Langer', 8114: 'Lee Carseldine', 8399: 'Shane Harwood', 8581: 'Ashok Sharma', 17741: 'Parag More', 45582: 'Aditya Angle', 48571: 'Rob Quiney', 51487: 'Abdulahad Malek', 52809: 'Mohammed Arif', 54284: 'Gajendra Singh', 59638: 'Pushkaraj Chavan', 8040: 'Sanjay Bangar', 9801: 'Wilkin Mota', 8077: 'Ranadeb Bose', 2121: 'Stephen Fleming', 4073: 'Makhaya Ntini', 7528: 'Vidyut Sivaramakrishnan', 51453: 'Palani  Amarnath', 24672: 'Mashrafe Mortaza', 48744: 'Arindam Ghosh', 58340: 'Shoaib Shaikh', 53565: 'Shoaib Ahmed', 6354: 'Morne van Wyk', 7221: 'Graham Napier', 6259: 'Simon Katich', 7130: 'Wasim Jaffer', 47207: 'Dillon du Preez', 13029: 'Sourav Sarkar', 19647: 'Mohammad Hafeez', 8244: 'Ashley Noffke', 2292: 'Sunil Joshi', 4175: 'Pankaj Dharmani', 3329: 'Darren Lehmann', 12402: 'Brett Geeves', 2101: 'Glenn McGrath', 7447: 'Dominic Thornely', 2228: 'Shaun Pollock', 7700: 'Musavir Khote', 2120: 'Shivnarine Chanderpaul', 9257: 'Kamran Akmal', 4169: 'Shahid Afridi', 8270: 'Shoaib Malik', 19627: 'Mohammad Asif', 52946: 'Vikrant Yeligati', 46688: 'Doddapaneni Kalyankrishna', 6405: 'Ramnaresh Sarwan', 48128: 'Sohail Tanvir', 5413: 'Nuwan Zoysa', 11647: 'Salman Butt', 44908: 'Umar Gul', 7723: 'Gagandeep Singh', 19596: 'Misbah-ul-Haq', 50809: 'Paidikalva Vijaykumar', 10557: 'Devraj Patil', 12810: 'Uday Kaul', 48520: 'Chamara Kapugedera', 10421: 'Tatenda Taibu', 7979: 'Jagadeesh Arunkumar', 5649: 'Shoaib Akhtar', 54389: 'PM Sarvesh Kumar', 7668: 'Rajesh Pawar', 45159: 'Abdur Razzak', 8197: 'Chamara Silva', 49330: 'Halhadar Das', 15389: 'Mayank Tehlan', 6343: 'Andre Nel', 10439: 'Younis Khan'}

def get_series_data_from_bucket(series_id):
  bucket_name = 't20_sense_series_info'
  file_path = f's_{series_id}_data.pkl'
  bucket = storage_client.get_bucket(bucket_name)
  # Get the blob (file) from the bucket
  blob = bucket.blob(file_path)
  # Download the pickle file data as bytes
  pickled_data = blob.download_as_bytes()
  # Load the pickled data
  loaded_data = pickle.loads(pickled_data)
  return loaded_data

def get_match_data_from_bucket(series_id, match_id):
  bucket_name = 't20_sense_match_info'
  file_path = f's_{series_id}_m_{match_id}_data.pkl'
  bucket = storage_client.get_bucket(bucket_name)
  # Get the blob (file) from the bucket
  blob = bucket.blob(file_path)
  # Download the pickle file data as bytes
  pickled_data = blob.download_as_bytes()
  # Load the pickled data
  loaded_data = pickle.loads(pickled_data)
  return loaded_data

def get_man_of_the_match(series_id, match_id):
  url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/home?lang=en&seriesId={series_id}&matchId={match_id}"
  response = requests.get(url)
  mom = response.json()['content']['matchPlayerAwards'][0]['player']['longName']
  return mom

def get_best_shots(series_id, match_id):
  url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/home?lang=en&seriesId={series_id}&matchId={match_id}"
  response = requests.get(url)
  bat_data = response.json()['content']['bestPerformance']['batsmen']
  perf_bat_inn1 = f"{bat_data[0]['teamAbbreviation']} - {bat_data[0]['player']['longName']} with {bat_data[0]['shot']} shot scoring {bat_data[0]['shotRuns']} out of {bat_data[0]['runs']} runs"
  perf_bat_inn2 = f"{bat_data[1]['teamAbbreviation']} - {bat_data[1]['player']['longName']} with {bat_data[1]['shot']} shot scoring {bat_data[1]['shotRuns']} out of {bat_data[1]['runs']} runs"
  return perf_bat_inn1, perf_bat_inn2

def fun_best_bowl_peformance(series_id, match_id):
  # Bowlers Stats Format -> Overs-Maidens-Runs-Wickets
  data = get_match_data_from_bucket(series_id, match_id)
  data = data['content']['bestPerformance']['bowlers']
  data0 = data[0] # 1st bowler
  data1 = data[1] # 2nd bowler
  bowl_perf_inn_1 = f"{data0['teamAbbreviation']} - {data0['player']['longName']} - [{data0['overs']}-{data0['maidens']}-{data0['conceded']}-{data0['wickets']}] conceding {data0['dots']} dots and Econ. {data0['economy']}"
  bowl_perf_inn_2 = f"{data1['teamAbbreviation']} - {data1['player']['longName']} - [{data1['overs']}-{data1['maidens']}-{data1['conceded']}-{data1['wickets']}] conceding {data1['dots']} dots and Econ. {data1['economy']}"
  return bowl_perf_inn_1, bowl_perf_inn_2

def round_float(value):
    if isinstance(value, (int, float)):
        return round(value, 2)

def batting_impact_points(series_id,match_id):

  url_p = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/home?lang=en&seriesId={series_id}&matchId={match_id}"
  output_p = requests.get(url_p)
  content = output_p.json()['content']
  partnership_df = pd.DataFrame(columns=['innings', 'player1ID', 'player1', 'player2ID', 'player2','player_out_id', 'player1_runs', 'player1_balls','player2_runs', 'player2_balls', 'partnershipRuns', 'partnershipBalls'])
  f = 0
  for k in range(0, 2):
    partnerships = content['innings'][k]['inningPartnerships']
    for p in range(0, len(partnerships)):
        partnership_df.loc[f, 'innings'] = k + 1
        partnership_df.loc[f, 'player1ID'] = partnerships[p]['player1']['id']
        partnership_df.loc[f, 'player1'] = partnerships[p]['player1']['longName']
        partnership_df.loc[f, 'player2ID'] = partnerships[p]['player2']['id']
        partnership_df.loc[f, 'player2'] = partnerships[p]['player2']['longName']
        partnership_df.loc[f, 'player_out_id'] = partnerships[p]['outPlayerId']
        partnership_df.loc[f, 'player1_runs'] = partnerships[p]['player1Runs']
        partnership_df.loc[f, 'player1_balls'] = partnerships[p]['player1Balls']
        partnership_df.loc[f, 'player2_runs'] = partnerships[p]['player2Runs']
        partnership_df.loc[f, 'player2_balls'] = partnerships[p]['player2Balls']
        partnership_df.loc[f, 'partnershipRuns'] = partnerships[p]['runs']
        partnership_df.loc[f, 'partnershipBalls'] = partnerships[p]['balls']
        f += 1
  partnership_df['player_out'] = partnership_df['player_out_id'].map(ipl_player_dictionary).fillna("not out")
  for index, row in partnership_df.iterrows():
    partnership_df.at[index, 'p1_contrib'] = (row['player1_runs'] * 100 / row['partnershipRuns']) if row['partnershipRuns'] != 0 else 0
    partnership_df.at[index, 'p2_contrib'] = (row['player2_runs'] * 100 / row['partnershipRuns']) if row['partnershipRuns'] != 0 else 0
    partnership_df.at[index, 'player1_SR'] = (row['player1_runs'] * 100 / row['player1_balls']) if row['player1_balls'] != 0 else 0
    partnership_df.at[index, 'player2_SR'] = (row['player2_runs'] * 100 / row['player2_balls']) if row['player2_balls'] != 0 else 0

  player_dict={}
  # matches_ids=match_ids(series_id)
  # for match_id in matches_ids:
  url1=f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/home?lang=en&seriesId={series_id}&matchId={match_id}"
  output1=requests.get(url1)
  for i in range(0,2):
    try:
      matches1 = output1.json()['content']['matchPlayers']['teamPlayers'][i]['players']
      for j in range(0,len(matches1)):
        player_id=matches1[j]['player']['id']
        player_name=matches1[j]['player']['longName']
        player_dict[player_id] = player_name
    except:
      continue
  df = pd.DataFrame(list(player_dict.items()), columns=['player id', 'player name'])
  df['runs']=0
  df['balls']=0
  df['impact_points']=0
  df['runs_imp']=0
  df['fours_imp']=0
  df['sixes_imp']=0
  team_1_total = 0
  team_2_total = 0
  team1_balls = 0
  team2_balls = 0
  wkts1=0
  wkts2=0
  
  for innings in range(1,3):
    try:
      url =f'https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments?lang=en&seriesId={series_id}&matchId={match_id}&inningNumber={innings}&commentType=ALL&sortDirection=DESC&fromInningOver=-1'
      output=requests.get(url)
      matches = output.json()['comments']
      impact_points=0
      # Performance_score=0
      for i in range(0,len(matches)):
        over=matches[i]['overNumber']
        oversActual=matches[i]['oversActual']
        totalruns=matches[i]['totalRuns']
        bowler_id=matches[i]['bowlerPlayerId']
        batsman_id=matches[i]['batsmanPlayerId']
        batsman1_id=batsman_id
        batsman_runs=matches[i]['batsmanRuns']
        wides=matches[i]['wides']
        noballs=matches[i]['noballs']
        byes=matches[i]['byes']
        legbyes=matches[i]['legbyes']
        penalties=matches[i]['penalties']
        wicket=matches[i]['isWicket']

        if(batsman_runs==0 and wides==0):
          dot = 1
        else:
          dot = 0
        impact_points=0
        runs_imp=0
        four_imp=0
        sixes_imp=0
        if(wides>0):
          ball=0
        else:
          ball=1

        ##Runrate
        if(innings==1):
          team_1_total=team_1_total + totalruns
          team1_balls=team1_balls+ball
          CRR1=team_1_total*6/team1_balls
        else:
          target=team_1_total
          team_2_total=team_2_total + totalruns
          team2_balls=team2_balls+ball
          required_runs=target-team_2_total
          required_rr=required_runs*6/(120-team2_balls)
          CRR2=team_2_total*6/team2_balls

        ##Impact points
        if(batsman_runs==0):
          impact_points=0
          runs_imp=0
          four_imp=0
          sixes_imp=0
        elif(batsman_runs==1):
          impact_points=1
          runs_imp=1
        elif(batsman_runs==2):
          impact_points=2
          runs_imp=2
        elif(batsman_runs==3):
          impact_points=3
          runs_imp=3
        elif(batsman_runs==4):
          impact_points=4.5
          four_imp=4.5
        elif(batsman_runs==6):
          impact_points=7
          sixes_imp=7


        # k = i + 1
        batsman2_id = None
        check=0
        p=k
        while(check):
          b_id = matches[p]['batsmanPlayerId']
          if b_id != batsman_id:
            batsman2_id = b_id
            check=1
            break
          p += 1

        ##Wicket
        if(wicket==True):
          outplayer_id=matches[i]['outPlayerId']
          next_batsman_id=matches[i+1]['batsmanPlayerId']
          if(next_batsman_id == batsman2_id or batsman_id):
            check=0
            while(check):
              p = k
              b_id = matches[p]['batsmanPlayerId']
              if(b_id != batsman2_id or batsman_id):
                next_batsman_id = b_id
                check=1
                break
              p += 1
          if(innings==1):
            wkts1 += 1
            if(wkts1==1):
              df.loc[df['player id'] == outplayer_id, 'CRR_when_came'] = 0
              df.loc[df['player id'] == batsman2_id, 'CRR_when_came'] = 0
            else:
              df.loc[df['player id'] == outplayer_id, 'CRR_when_out']= CRR1
              df.loc[df['player id'] == outplayer_id, 'team_score']= team_1_total
              df.loc[df['player id'] == outplayer_id, 'team_balls']= team1_balls
              df.loc[df['player id'] == next_batsman_id, 'CRR_when_came']= CRR1
            CRR1_arrived=CRR1

          if(innings==2):
            wkts2 += 1
            next_batsman_id=matches[i+1]['batsmanPlayerId']
            if(next_batsman_id == batsman2_id or batsman_id):
              check=0
              while(check):
                p = k
                b_id = matches[p]['batsmanPlayerId']
                if(b_id != batsman2_id or batsman_id):
                  next_batsman_id = b_id
                  check=1
                  break
                p += 1
            df.loc[df['player id'] == outplayer_id, 'team_score']= team_2_total
            df.loc[df['player id'] == outplayer_id, 'team_balls']= team2_balls
            if(wkts2!=1):
              df.loc[df['player id'] == outplayer_id, 'RRR_when_came']=req_rr
            if(wkts2==1):
              df.loc[df['player id'] == outplayer_id, 'RRR_when_came']=CRR1
              df.loc[df['player id'] == batsman2_id, 'RRR_when_came']=CRR1
              df.loc[df['player id'] == outplayer_id, 'CRR_when_came']=0
              df.loc[df['player id'] == batsman2_id, 'CRR_when_came']=0
            df.loc[df['player id'] == outplayer_id, 'CRR_when_out']= CRR2
            df.loc[df['player id'] == next_batsman_id, 'CRR_when_came']= CRR2
            df.loc[df['player id'] == outplayer_id, 'RRR_when_out']= required_rr
            req_rr=required_rr

        if(innings==2):
          if(oversActual==0.1):
            df.loc[df['player id'] == batsman_id, 'RRR_when_came']=CRR1
            # df.loc[df['player id'] == batsman2_id, 'RRR_when_came']=CRR1


        df.loc[df['player id']==batsman_id,'innings']=innings
        df.loc[df['player id'] == batsman_id, 'runs'] = df.loc[df['player id'] == batsman_id,'runs'] + batsman_runs
        df.loc[df['player id'] == batsman_id, 'balls'] = df.loc[df['player id'] == batsman_id,'balls'] + ball
        r=0
        dp=0
        if(over<7):
          r=0.5
        elif(over>16 and over<19):
          r=1
          if(dot==1):
            dp=-0.5
        elif(over>18):
          r=2
          if(dot==1):
            dp=-1
        else:
          r=0
        df.loc[df['player id'] == batsman_id, 'runs_imp']+= runs_imp
        # if(totalruns!=0):
        #   df.loc[df['player id'] == batsman_id, 'impact_points']+= impact_points + r
        # elif (batsman_runs==0 and wides==0):
        #   df.loc[df['player id'] == batsman_id, 'impact_points']+= impact_points + dp
        if(four_imp!=0):
          df.loc[df['player id'] == batsman_id, 'fours_imp']+= four_imp + r
        else:
          df.loc[df['player id'] == batsman_id, 'fours_imp']+= four_imp
        if(sixes_imp!=0):
          df.loc[df['player id'] == batsman_id, 'sixes_imp']+= sixes_imp + r
        else:
          df.loc[df['player id'] == batsman_id, 'sixes_imp']+= sixes_imp
        # b_df.loc[b_df['player id'] == bowler_id, 'runs'] = b_df.loc[b_df['player id'] == bowler_id,'runs'] + batsman_runs
        # b_df.loc[b_df['player id'] == bowler_id, 'Performance_score']+= Performance_score

      df['impact_points']=df['runs_imp'] + df['fours_imp'] + df['sixes_imp']
      df['SR'] = (df['runs']*100/df['balls']).round(2)

      for i in range(len(df)):
        p=0
        p=df['runs'][i]/10
        df['impact_points'][i]+=p*2
      target=df.loc[df['innings'] == 1, 'runs'].sum()
      target_sr=target/1.2
    except:
      continue

  # for j in range(0,len(partnership_df)):

  for j in range(len(df)):
    if(df['innings'][j]==1):
      first_total=df['runs'].sum()
      first_balls=df['balls'].sum()
      first_SR=first_total*6/first_balls
      if(df['SR'][j]<(first_SR)/2):
        df['impact_points'][j]-=5
      elif(df['SR'][j]<first_SR):
        df['impact_points'][j]-=2
      elif(df['SR'][j]>=1.5*(first_SR)):
        df['impact_points'][j]+=2
      elif(df['SR'][j]>2*(first_SR)):
        df['impact_points'][j]+=5
    else:
      if(df['SR'][j]<(target_sr)/2):
        df['impact_points'][j]-=5
      elif(df['SR'][j]<target_sr):
        df['impact_points'][j]-=2
      elif(df['SR'][j]>=1.5*(target_sr)):
        df['impact_points'][j]+=2
      elif(df['SR'][j]>2*(target_sr)):
        df['impact_points'][j]+=5
    df1 = df[df['impact_points'] != 0]
    df1['CRR_when_out']=df1['CRR_when_out'].fillna(" - ")
    df1['RRR_when_came']=df1['RRR_when_came'].fillna(" - ")
    df1['CRR_when_out']=(df1['CRR_when_out']).apply(round_float)
    # df1['RRR_when_came']=(df1['RRR_when_came']).apply(round_float)
    # df1['RRR_when_out']=(df1['RRR_when_out']).apply(round_float)
    # b_df1 = b_df[b_df['Performance_score'] != 0]
  return df1,partnership_df