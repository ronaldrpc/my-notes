from datetime import timedelta
from unittest import mock

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Note


class NoteModelTests(TestCase):
    def test_change_last_modified_date(self):
        """Test that the last modified date changes when the note is updated."""
        fake_time = timezone.now() - timedelta(days=1)

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = fake_time

            note = Note(title="Test Title 1", description="Test Description 1")
            note.save()
            self.assertEqual(note.last_modified_date, note.create_date)
        
        note.title = "Test Title 1.1"
        note.save()
        self.assertNotEqual(note.last_modified_date, note.create_date)
        self.assertTrue(note.last_modified_date > note.create_date)


class NoteIndexViewTests(TestCase):
    def test_no_notes(self):
        """Test if there are not any notes to show."""
        response = self.client.get(reverse('notes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No notes to show', html=True)  # This message comes from the template
        self.assertQuerysetEqual(response.context['notes'], [])

    def test_notes_exists(self):
        """Test if there are notes to show."""
        note_1 = Note.objects.create(title='Note Title 1', description='Note Description 1')
        note_2 = Note.objects.create(title='Note Title 2', description='Note Description 2')

        response = self.client.get(reverse('notes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['notes'].order_by('title'), [note_1, note_2])

    def test_no_archived_notes(self):
        """Test if there are not any archived notes to show."""
        response = self.client.get(reverse('notes:index_archived', args=('archived',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No notes to show', html=True)
        self.assertQuerysetEqual(response.context['notes'], [])
    
    def test_archived_note(self):
        """Test if an archived note shows in their respective view."""
        note = Note.objects.create(title='Note archived', description='Note archiveddddd')
        note.is_active = False
        note.save()

        response = self.client.get(reverse('notes:index_archived', args=('archived',)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, note.title)
        self.assertQuerysetEqual(response.context['notes'], [note])


class NoteDetailViewTests(TestCase):
    def test_note_not_found(self):
        """Test if a given id note actually exists."""
        id = 123
        url = reverse('notes:note-update', args=(id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_note_found(self):
        """Test if a given id belongs to an existing note."""
        note = Note.objects.create(title='Note Title', description='Note Description')
        url = reverse('notes:note-update', args=(note.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, note.title)


class NoteCreateViewTests(TestCase):
    def setUp(self):
        self.url_create = reverse('notes:note-create')  # notes/note/create/

    def test_get_create_note(self):
        """Test loading create template."""
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create note', html=True)
    
    def test_post_create_note(self):
        """Test if can create a note from create template."""
        data = {'title': 'Note', 'description': 'Noteeeeeeee'}
        response = self.client.post(self.url_create, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        note = Note.objects.filter(title=data.get('title'))
        self.assertTrue(note)


class NoteUpdateViewTests(TestCase):
    def setUp(self):
        """Setting things up for the tests."""
        self.note = Note.objects.create(title='Note', description='Note')
        self.url = reverse('notes:note-update', args=(self.note.id,))

    def test_update_note(self):
        """Test if can update a note from update template and save changes."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        new_data = {'title': 'Note', 'description': 'Noteeeeeeee'}
        response = self.client.post(self.url, data=new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data['description'], response.context['note'].description)

    def test_change_status_note(self):
        """Test if can change note status from update template."""
        new_data = {'is_active': False}
        response = self.client.post(self.url, data=new_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_data['is_active'], response.context['note'].is_active)
