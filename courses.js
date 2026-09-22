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
      title: "Python Fundamentals",
      subtitle: "Multimedia course",
      description: "Programming basics for multimedia students, from your first print() to writing your own functions.",
      hue: 172,
      totalWeeks: 10,
      weeks: [
        {
          week: 1,
          title: "Introduction to Python",
          topics: ["output & input", "variables", "operators", "collections", "control flow", "functions"],
          file: "decks/multimedia/Week ⇔ 01/Session ⇔ 01.html",
          date: "2026-09-22",
          duration: "75 min"
        }
        // ,{ week: 2, title: "…", topics: ["…"], file: "decks/multimedia/Week ⇔ 02/Session ⇔ 02.html", date: "2026-09-29" }
      ]
    },

    {
      id: "data-structures",
      title: "Data Structures with C++",
      subtitle: "Faculty of IT and CS",
      description: "Core data structures built by hand in C++, one hands-on session at a time.",
      hue: 262,
      totalWeeks: 10,
      weeks: [
        {
          week: 1,
          title: "From Structured Programming to Functions",
          topics: ["sequence", "selection", "repetition", "functions", "5 hands-on tasks"],
          file: "decks/data-structures/Week ⇔ 01/Session ⇔ 01.html",
          date: "2026-09-22",
          duration: "75 min"
        }
        // ,{ week: 2, title: "…", topics: ["…"], file: "decks/data-structures/Week ⇔ 02/Session ⇔ 02.html", date: "2026-09-29" }
      ]
    }
  ]
};
