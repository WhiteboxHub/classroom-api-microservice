db = db.getSiblingDB('social_profiles');

db.students.insertMany([
    {
        student_id: 1,
        name: "Alice Johnson",
        social_links: {
            facebook: "https://facebook.com/alicejohnson",
            linkedin: "https://linkedin.com/in/alicejohnson"
        }
    },
    {
        student_id: 2,
        name: "Bob Smith",
        social_links: {
            facebook: "https://facebook.com/bobsmith",
            twitter: "https://twitter.com/bobsmith"
        }
    },
    {
        student_id: 3,
        name: "Charlie Brown",
        social_links: {
            linkedin: "https://linkedin.com/in/charliebrown"
        }
    }
]);
