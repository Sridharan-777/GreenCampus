"""
Seed script to populate initial categories, sample users, badges, reports, events, and rewards.
Run with: python seed_data.py
"""
import os
import django
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greencampus.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from core.models import UserProfile, EcoBadge, UserBadge, PointActivity
from reports.models import WasteCategory, WasteReport
from events.models import CampaignCategory, Campaign, EventRSVP
from analytics.models import RewardItem, RewardRedemption


def create_demo_image(text, bg_color=(16, 185, 129), size=(600, 360)):
    image = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(image)
    # Draw simple text / shapes
    draw.rectangle([20, 20, size[0]-20, size[1]-20], outline=(255, 255, 255), width=3)
    # Try default font
    draw.text((40, size[1]//2 - 10), text, fill=(255, 255, 255))
    
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=85)
    return ContentFile(buffer.getvalue())


def seed():
    print("[*] Seeding GreenCampus Initial Data...")

    # 1. Superuser / Admin
    admin_user, _ = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@greencampus.edu',
        'first_name': 'Dr. Sarah',
        'last_name': 'Jenkins',
        'is_staff': True,
        'is_superuser': True
    })
    admin_user.set_password('admin123')
    admin_user.save()
    admin_user.profile.role = 'admin'
    admin_user.profile.department = 'Sustainability Cell'
    admin_user.profile.eco_points = 1200
    admin_user.profile.save()

    # 2. Marshal User (Staff)
    marshal_user, _ = User.objects.get_or_create(username='marshal_alex', defaults={
        'email': 'alex@greencampus.edu',
        'first_name': 'Alex',
        'last_name': 'Rivera',
        'is_staff': True
    })
    marshal_user.set_password('alex123')
    marshal_user.save()
    marshal_user.profile.role = 'marshal'
    marshal_user.profile.department = 'Campus Facilities'
    marshal_user.profile.eco_points = 650
    marshal_user.profile.save()

    # 3. Student Champions (Team 7 demo students)
    students_data = [
        ('priya_sharma', 'Priya', 'Sharma', 'Computer Science', 'Hostel A', 480),
        ('rahul_verma', 'Rahul', 'Verma', 'Environmental Engg', 'Hostel C', 390),
        ('ananya_sen', 'Ananya', 'Sen', 'Biotechnology', 'Hostel B', 310),
        ('kavya_patel', 'Kavya', 'Patel', 'Mechanical Engg', 'Hostel A', 220),
        ('rohit_kumar', 'Rohit', 'Kumar', 'Civil Engineering', 'Main Quad', 150),
    ]

    created_students = []
    for uname, fname, lname, dept, hostel, pts in students_data:
        u, _ = User.objects.get_or_create(username=uname, defaults={
            'email': f"{uname}@campus.edu",
            'first_name': fname,
            'last_name': lname
        })
        u.set_password('student123')
        u.save()
        u.profile.department = dept
        u.profile.hostel_or_block = hostel
        u.profile.eco_points = pts
        u.profile.save()
        created_students.append(u)

    # 4. Badges
    badges_data = [
        ("Waste Warrior", "Reported and resolved over 5 waste hot-spots.", "fa-recycle", 100, "#10b981"),
        ("Eco Scout", "Participated in at least 2 campus clean-up drives.", "fa-leaf", 50, "#06b6d4"),
        ("Zero Waste Champion", "Accumulated over 300 Eco-Points through verified reports.", "fa-award", 250, "#f59e0b"),
        ("Green Guardian", "Achieved top level eco-ranking on university leaderboard.", "fa-shield-halved", 500, "#8b5cf6"),
    ]
    badges_objs = []
    for name, desc, icon, pts, color in badges_data:
        b, _ = EcoBadge.objects.get_or_create(name=name, defaults={
            'description': desc,
            'icon': icon,
            'points_required': pts,
            'badge_color': color
        })
        badges_objs.append(b)

    # Award badges to students
    if created_students and badges_objs:
        UserBadge.objects.get_or_create(user=created_students[0], badge=badges_objs[0])
        UserBadge.objects.get_or_create(user=created_students[0], badge=badges_objs[2])
        UserBadge.objects.get_or_create(user=created_students[1], badge=badges_objs[0])
        UserBadge.objects.get_or_create(user=created_students[1], badge=badges_objs[1])

    # 5. Waste Categories
    categories_data = [
        ("Plastic Waste", "plastic", "fa-bottle-water", "#3b82f6", 30, 2.50),
        ("Organic & Food", "organic", "fa-apple-whole", "#10b981", 20, 1.20),
        ("Paper & Cardboard", "paper", "fa-newspaper", "#f59e0b", 25, 1.80),
        ("E-Waste", "e-waste", "fa-microchip", "#8b5cf6", 50, 4.00),
        ("Metal & Cans", "metal", "fa-can-food", "#64748b", 35, 3.20),
        ("Glass Bottles", "glass", "fa-wine-bottle", "#06b6d4", 30, 1.50),
    ]
    cat_objs = {}
    for name, slug, icon, color, pts, co2 in categories_data:
        c, _ = WasteCategory.objects.get_or_create(slug=slug, defaults={
            'name': name,
            'icon': icon,
            'badge_color': color,
            'base_eco_points': pts,
            'co2_saved_per_kg': co2
        })
        cat_objs[slug] = c

    # 6. Sample Waste Reports (Module 1)
    reports_data = [
        ("Overflowing plastic bottles near Central Cafeteria", "plastic", created_students[0], "Central Cafeteria Courtyard", 4.5, "high", "cleaned", 40, (59, 130, 246)),
        ("Discarded cardboard boxes behind Science Lab 3", "paper", created_students[1], "Science Block East Wing", 6.0, "medium", "cleaned", 35, (245, 158, 11)),
        ("Old laptop chargers & broken keyboards near CS Dept", "e-waste", created_students[2], "Computer Science Ground Floor", 3.2, "medium", "in_progress", 0, (139, 92, 246)),
        ("Organic food waste bin overflow in Hostel B Dining", "organic", created_students[3], "Hostel B Mess Lawn", 8.0, "critical", "cleaned", 50, (16, 185, 129)),
        ("Crushed beverage cans along Sports Complex track", "metal", created_students[4], "Athletics Track Pavilion", 2.8, "low", "pending", 0, (100, 116, 139)),
    ]

    for title, cat_slug, user_obj, loc, weight, urgency, status, pts, rgb in reports_data:
        img_content = create_demo_image(f"Report: {title[:28]}", bg_color=rgb)
        clean_img_content = create_demo_image("Resolved Clean Area", bg_color=(16, 185, 129)) if status == 'cleaned' else None

        report = WasteReport(
            title=title,
            reported_by=user_obj,
            category=cat_objs.get(cat_slug),
            location_name=loc,
            description=f"Identified unsegregated waste around {loc}. Needs immediate collection.",
            estimated_weight_kg=weight,
            urgency=urgency,
            status=status,
            points_awarded=pts,
            verified_by=marshal_user if status == 'cleaned' else None,
            verification_notes="Maintenance team cleared the site and segregated waste." if status == 'cleaned' else ""
        )
        report.image.save(f"report_{cat_slug}.jpg", img_content, save=False)
        if clean_img_content:
            report.cleaned_image.save(f"clean_{cat_slug}.jpg", clean_img_content, save=False)
        report.save()

    # 7. Campaign Categories & Events (Module 2)
    campaign_cats = [
        ("Clean-up Drive", "cleanup", "fa-broom", "#10b981"),
        ("E-Waste Rally", "e-waste-rally", "fa-recycle", "#8b5cf6"),
        ("Tree Plantation", "tree-plantation", "fa-tree", "#84cc16"),
        ("Zero Waste Workshop", "workshop", "fa-chalkboard-user", "#f59e0b"),
    ]
    camp_cat_objs = {}
    for name, slug, icon, col in campaign_cats:
        cc, _ = CampaignCategory.objects.get_or_create(slug=slug, defaults={
            'name': name,
            'icon': icon,
            'color': col
        })
        camp_cat_objs[slug] = cc

    now = timezone.now()
    events_data = [
        ("Campus Mega Clean-up & Plastic Segregation Drive", "cleanup", admin_user, "Central Quad & Amphitheater", now + timedelta(days=3), now + timedelta(days=3, hours=4), 50, 75, (5, 150, 105)),
        ("Annual E-Waste Collection & Safe Disposal Fair", "e-waste-rally", marshal_user, "Student Center Atrium", now + timedelta(days=7), now + timedelta(days=7, hours=6), 40, 60, (124, 58, 237)),
        ("Green Campus 100 Trees Plantation Initiative", "tree-plantation", admin_user, "Botanical Gardens & North Boundary", now + timedelta(days=12), now + timedelta(days=12, hours=5), 60, 100, (101, 163, 13)),
    ]

    for title, cat_slug, org, loc, s_date, e_date, target, pts, rgb in events_data:
        banner_content = create_demo_image(f"Event: {title[:25]}", bg_color=rgb, size=(800, 400))
        c = Campaign(
            title=title,
            category=camp_cat_objs.get(cat_slug),
            organizer=org,
            location=loc,
            start_date=s_date,
            end_date=e_date,
            target_volunteers=target,
            eco_points_reward=pts,
            description="Join our team of students and faculty marshals to create a cleaner and greener environment. Gloves and sorting kits provided.",
            status="upcoming",
            is_active=True
        )
        c.banner_image.save(f"event_{cat_slug}.jpg", banner_content, save=False)
        c.save()

        # Add sample RSVPs
        for stu in created_students[:3]:
            EventRSVP.objects.get_or_create(campaign=c, user=stu, defaults={'volunteer_role': 'Eco Volunteer'})

    # 8. Rewards Store Items (Module 3)
    rewards_data = [
        ("Cafeteria Green Lunch Voucher (₹150)", "Redeem for a fresh meal or smoothie at Central Campus Cafeteria.", 120, "fa-utensils", "Campus Dining Services", 45),
        ("Reusable Stainless Steel Eco Bottle (750ml)", "Ditch single-use plastic with this insulated campus-branded steel bottle.", 250, "fa-bottle-water", "Sustainability Office", 20),
        ("Official Campus Sustainability Certificate", "Dean-signed certificate recognizing your volunteer hours & eco-contributions.", 200, "fa-certificate", "Dean of Student Affairs", 100),
        ("Organic Canvas Tote Bag", "Durable zero-waste shopping and book tote bag.", 80, "fa-bag-shopping", "Eco Club", 35),
    ]

    for title, desc, cost, icon, sponsor, stock in rewards_data:
        RewardItem.objects.get_or_create(title=title, defaults={
            'description': desc,
            'points_cost': cost,
            'icon': icon,
            'sponsor': sponsor,
            'available_stock': stock,
            'is_active': True
        })

    print("[SUCCESS] Seeding completed successfully!")
    print("\nDefault Accounts Created:")
    print("  * Admin:     username='admin', password='admin123'")
    print("  * Marshal:   username='marshal_alex', password='alex123'")
    print("  * Students:  username='priya_sharma', password='student123' (and others)")


if __name__ == '__main__':
    seed()
