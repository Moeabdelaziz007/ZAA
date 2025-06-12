import { render, screen } from '@testing-library/react';
import { EmotionChart } from '../../components/EmotionChart';

describe('EmotionChart Component', () => {
  const mockData = [
    { date: '2024-01-01', emotion: 'happy', confidence: 0.9 },
    { date: '2024-01-02', emotion: 'sad', confidence: 0.7 },
    { date: '2024-01-03', emotion: 'neutral', confidence: 0.8 },
  ];

  test('renders chart with data', () => {
    render(<EmotionChart data={mockData} />);
    
    // Check if chart container is rendered
    expect(screen.getByTestId('emotion-chart')).toBeInTheDocument();
    
    // Check if all data points are rendered
    mockData.forEach(point => {
      expect(screen.getByText(point.emotion)).toBeInTheDocument();
    });
  });

  test('renders empty state', () => {
    render(<EmotionChart data={[]} />);
    
    expect(screen.getByText(/no data available/i)).toBeInTheDocument();
  });

  test('handles loading state', () => {
    render(<EmotionChart data={mockData} isLoading={true} />);
    
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  test('handles error state', () => {
    const error = 'Failed to load data';
    render(<EmotionChart data={mockData} error={error} />);
    
    expect(screen.getByText(error)).toBeInTheDocument();
  });
}); 