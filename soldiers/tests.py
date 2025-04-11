from django.test import TestCase
from .models import Soldier
from battalions.models import battalion, battalion_group
from django.core.exceptions import ValidationError

class SoldierModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.battalion = battalion.objects.create(
            name="گردان تست",
            code="123"
        )
        
        self.battalion_group = battalion_group.objects.create(
            name="گروهان تست",
            code="456",
            battalion=self.battalion
        )
        
        self.soldier = Soldier.objects.create(
            name="علی",
            family="محمدی",
            fathers_name="محمد",
            National_Code="1234567890",
            Grade="کارشناسی",
            marital_status="مجرد",
            phone_number="09123456789",
            Gordan=self.battalion,
            battalion_group=self.battalion_group
        )

    def test_soldier_creation(self):
        """Test creating a soldier instance"""
        self.assertEqual(self.soldier.name, "علی")
        self.assertEqual(self.soldier.family, "محمدی")
        self.assertEqual(self.soldier.National_Code, "1234567890")
        self.assertEqual(self.soldier.Grade, "کارشناسی")

    def test_soldier_str_representation(self):
        """Test the string representation of Soldier model"""
        expected_str = "علی - محمدی - 1234567890"
        self.assertEqual(str(self.soldier), expected_str)

    def test_soldier_score_calculations(self):
        """Test score calculations for a soldier"""
        self.soldier.discipline_score = 2.0
        self.soldier.basij_experience = 24  # 24 months
        self.soldier.council_experience = 12  # 12 months
        self.soldier.ideological_score = 1.0
        self.soldier.shooting_score = 2.0
        self.soldier.battalion_activity = 2.5
        self.soldier.battalion_sample = True
        self.soldier.quran_memorization = 3
        self.soldier.nahj_memorization = True
        self.soldier.sajjadiya_memorization = True
        
        # Save to update any calculated fields
        self.soldier.save()
        
        # Verify individual scores
        self.assertEqual(self.soldier.discipline_score, 2.0)
        self.assertEqual(self.soldier.basij_experience, 24)
        self.assertEqual(self.soldier.shooting_score, 2.0)

    def test_invalid_national_code(self):
        """Test validation for invalid National Code"""
        with self.assertRaises(ValidationError):
            invalid_soldier = Soldier.objects.create(
                name="رضا",
                family="احمدی",
                National_Code="123"  # Invalid length
            )
            invalid_soldier.full_clean()

    def test_phone_number_validation(self):
        """Test phone number validation"""
        with self.assertRaises(ValidationError):
            invalid_soldier = Soldier.objects.create(
                name="حسن",
                family="کریمی",
                phone_number="123"  # Invalid phone number
            )
            invalid_soldier.full_clean()

    def test_battalion_relationship(self):
        """Test the relationship between Soldier and Battalion"""
        self.assertEqual(self.soldier.Gordan, self.battalion)
        self.assertEqual(self.soldier.battalion_group, self.battalion_group)

    def test_default_values(self):
        """Test default values for boolean and numeric fields"""
        new_soldier = Soldier.objects.create(
            name="محسن",
            family="رضایی"
        )
        
        self.assertFalse(new_soldier.willing_to_learn)
        self.assertFalse(new_soldier.Amriye)
        self.assertEqual(new_soldier.discipline_score, 0)
        self.assertEqual(new_soldier.basij_experience, 0)
        self.assertEqual(new_soldier.total_score, 0)
