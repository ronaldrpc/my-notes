from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from notes.models import Note


class NoteAPIViewTests(APITestCase):
    """Testing api function views related to notes."""
    def setUp(self):
        Note.objects.create(title='Test Title', description='Test Description')

    def test_note_create(self):
        """Test if api can create a note."""
        data = {
            'title': 'Note title',
            'description': 'Note description',
        }
        response = self.client.post('/apidrf/notes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)


    def test_note_list(self):
        """Test if api shows existing notes."""
        list_notes = [
            {
                'title': 'Test Title',
                'description': 'Test Description',
            }
        ]
        response = self.client.get('/apidrf/notes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        minimal_data = []
        for note in response.data:
            minimal_data.append({'title': note['title'], 'description': note['description']})
        self.assertEqual(minimal_data, list_notes)

    def test_note_detail_put(self):
        """Test if PUT request can update a note."""
        new_data = {'title': 'New Title', 'description': 'New Description'}
        response = self.client.put('/apidrf/notes/1/',data=new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = Note.objects.get(pk=1)
        self.assertEqual(note.title, new_data['title'])
        self.assertEqual(note.description, new_data['description'])
    
    def test_note_detail_put_required(self):
        """Test if PUT request fails if any required field is not sent in the data."""
        new_data = {'title': 'New Title'}
        response = self.client.put('/apidrf/notes/1/',data=new_data, format='json')
        self.assertEqual(response.content, b'{"description":["This field is required."]}')

    def test_note_detail_delete(self):
        """Test api can accept delete request to remove a note."""
        response = self.client.delete('/apidrf/notes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)


