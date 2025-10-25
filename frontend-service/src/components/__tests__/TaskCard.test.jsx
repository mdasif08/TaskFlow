import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import TaskCard from '../TaskCard'

const mockTask = {
  id: 1,
  title: 'Test Task',
  description: 'Test Description',
  status: 'pending',
  priority: 'medium',
  created_at: '2024-01-01T00:00:00Z',
  assigned_user: {
    username: 'testuser'
  }
}

describe('TaskCard', () => {
  const mockOnEdit = jest.fn()
  const mockOnDelete = jest.fn()

  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('renders task information correctly', () => {
    render(<TaskCard task={mockTask} onEdit={mockOnEdit} onDelete={mockOnDelete} />)
    
    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Test Description')).toBeInTheDocument()
    expect(screen.getByText('PENDING')).toBeInTheDocument()
    expect(screen.getByText('MEDIUM')).toBeInTheDocument()
  })

  it('calls onEdit when edit button is clicked', () => {
    render(<TaskCard task={mockTask} onEdit={mockOnEdit} onDelete={mockOnDelete} />)
    
    const editButton = screen.getByTitle('Edit task')
    fireEvent.click(editButton)
    
    expect(mockOnEdit).toHaveBeenCalledWith(mockTask)
  })

  it('calls onDelete when delete button is clicked', () => {
    render(<TaskCard task={mockTask} onEdit={mockOnEdit} onDelete={mockOnDelete} />)
    
    const deleteButton = screen.getByTitle('Delete task')
    fireEvent.click(deleteButton)
    
    expect(mockOnDelete).toHaveBeenCalledWith(1)
  })
})
