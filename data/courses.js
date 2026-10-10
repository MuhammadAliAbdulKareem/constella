/* =====================================================================
   courses.js  —  الملف الوحيد اللي بتعدّل فيه كل أسبوع
   ---------------------------------------------------------------------
   إضافة سكشن جديد = 2 خطوات:
     1) حط ملف الـ deck في فولدر الكورس، مثلًا  decks/python/week-02.html
     2) انسخ سطر week جديد جوّه weeks بتاعة الكورس وعدّل عليه.

   الحقول:
     week      رقم الأسبوع (بيحدد مكان النجمة في الكوكبة)
     title     عنوان السكشن
     topics    قايمة المواضيع (البحث بيدوّر فيها)
     file      مسار ملف الـ deck
     date      "YYYY-MM-DD"  اختياري. أحدث تاريخ = "Latest session" في الصفحة الرئيسية
     duration  اختياري، زي "75 min"

   الكورس:
     hue          درجة لون الكورس من 0 لـ 360 (172 تركواز، 262 بنفسجي، 30 برتقالي، 340 وردي)
     totalWeeks   عدد أسابيع الترم (النجوم الباهتة هي الأسابيع اللي لسه جاية)
   ===================================================================== */

window.SITE = {
  title: "Constella",
  owner: "Muhammad Ali Abdul Kareem",
  affiliation: "Faculty of IT and CS, Sinai University",
  tagline: "Pick a star to open that week's interactive session. A new star lights up every week.",

  courses: [
    {
      id: "multimedia",
      title: "Multimedia Programming",
      titleAr: "برمجة الوسائط المتعددة",
      subtitle: "Faculty of IT and CS",
      description: "Interactive multimedia programming with Python, from core foundations to digital sound synthesis, sampling, and visual computing.",
      hue: 172,
      totalWeeks: 10,
      weeks: [
        {
          week: 1,
          title: "Introduction to Python",
          titleAr: "مقدمة إلى لغة بايثون",
          topics: ["output & input", "variables", "operators", "collections", "control flow", "functions"],
          keywordsAr: ["مقدمة", "بايثون", "طباعة", "مدخلات", "مخرجات", "متغيرات", "عمليات", "قوائم", "شروط", "دوال"],
          file: "decks/multimedia/Week ⇔ 01/Session ⇔ 01.html",
          codeFile: "decks/multimedia/Week ⇔ 01/session01_fundamentals.py",
          codeName: "session01_fundamentals.py",
          date: "2026-09-22",
          duration: "75 min",
          slides: 34
        },
        {
          week: 2,
          title: "Object-Oriented Programming (OOP) in Python",
          titleAr: "البرمجة كائنية التوجه (OOP) في بايثون",
          topics: ["classes & objects", "__init__() & self", "properties & del", "inheritance & super()", "polymorphism", "encapsulation"],
          keywordsAr: ["كائنات", "كائنية", "أوب", "فئات", "كلاس", "وراثة", "تعدد الأشكال", "تغليف", "خصائص"],
          file: "decks/multimedia/Week ⇔ 02/Session ⇔ 02.html",
          codeFile: "decks/multimedia/Week ⇔ 02/session02_oop.py",
          codeName: "session02_oop.py",
          date: "2026-09-29",
          duration: "75 min",
          slides: 17
        },
        {
          week: 3,
          title: "Digital Sound with Python",
          titleAr: "معالجة وتوليد الصوت الرقمي (Digital Sound)",
          topics: ["sine wave generation", "gain & loudness", "sampling rate (Fs)", "Nyquist theorem & aliasing", "quantization & bit depth", "DAC reconstruction & zero-order hold", "interactive audio labs"],
          keywordsAr: ["صوت رقمي", "موجة جيبية", "تردد", "أخذ العينات", "سامبلنج", "نظرية نايكوست", "تكميم", "عمق بت", "تحويل تناظري رقمي", "بايثون وسائط متعددة", "داك"],
          file: "decks/multimedia/Week ⇔ 03/Session ⇔ 03.html",
          codeFile: "decks/multimedia/Week ⇔ 03/session03_digital_sound.py",
          codeName: "session03_digital_sound.py",
          date: "2026-10-06",
          duration: "75 min",
          slides: 12
        }
      ]
    },

    {
      id: "data-structures",
      title: "Data Structures with C++",
      titleAr: "هياكل البيانات بلغة C++",
      subtitle: "Faculty of IT and CS",
      description: "Core data structures built by hand in C++, one hands-on session at a time.",
      hue: 262,
      totalWeeks: 10,
      weeks: [
        {
          week: 1,
          title: "From Structured Programming to Functions",
          titleAr: "من البرمجة الهيكلية إلى الدوال",
          topics: ["sequence", "selection", "repetition", "functions", "5 hands-on tasks"],
          keywordsAr: ["هياكل بيانات", "برمجة هيكلية", "دوال", "تكرار", "شروط", "سي بلس بلس", "مهام"],
          file: "decks/data-structures/Week ⇔ 01/Session ⇔ 01.html",
          codeFile: "decks/data-structures/Week ⇔ 01/Functions_Memory.cpp",
          codeName: "Functions_Memory.cpp",
          date: "2026-09-22",
          duration: "75 min",
          slides: 26
        },
        {
          week: 2,
          title: "Time Complexity & Growth Rates",
          titleAr: "التعقيد الزمني ومعدلات النمو",
          topics: ["Big-O notation", "8 complexity classes", "nested loops", "trace tables", "references", "capstone task"],
          keywordsAr: ["تعقيد زمني", "بيج أو", "حلقات متداخلة", "جداول التتبع", "مراجع", "تحليل خوارزميات"],
          file: "decks/data-structures/Week ⇔ 02/Session ⇔ 02.html",
          codeFile: "decks/data-structures/Week ⇔ 02/Complexity_BigO.cpp",
          codeName: "Complexity_BigO.cpp",
          date: "2026-09-29",
          duration: "75 min",
          slides: 20
        },
        {
          week: 3,
          title: "Arrays with OOP in C++",
          titleAr: "المصفوفات بالبرمجة كائنية التوجه (OOP)",
          topics: ["pointers & dynamic memory", "class ArrayList", "constructor & destructor", "safe input (readInt)", "insert & delete", "linear search", "grow() dynamic resize", "Rule of Three", "2D arrays", "student tasks"],
          keywordsAr: ["مصفوفات", "مصفوفة", "مؤشرات", "ذاكرة ديناميكية", "كلاس", "حذف", "إضافة", "بحث خطي", "قاعدة الثلاثة", "مصفوفات ثنائية", "سعة"],
          file: "decks/data-structures/Week ⇔ 03/Session ⇔ 03.html",
          codeFile: "decks/data-structures/Week ⇔ 03/ArrayList.cpp",
          codeName: "ArrayList.cpp",
          date: "2026-10-06",
          duration: "75 min",
          slides: 33
        }
        // ,{ week: 4, title: "…", topics: ["…"], file: "decks/data-structures/Week ⇔ 04/Session ⇔ 04.html", date: "2026-10-13" }
      ]
    }
  ]
};
