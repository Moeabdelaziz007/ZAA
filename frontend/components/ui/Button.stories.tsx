import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'UI/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline', 'ghost', 'link'],
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    isLoading: {
      control: 'boolean',
    },
    isDisabled: {
      control: 'boolean',
    },
    isFullWidth: {
      control: 'boolean',
    },
    leftIcon: {
      control: 'text',
    },
    rightIcon: {
      control: 'text',
    },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'زر رئيسي',
    variant: 'primary',
    size: 'md',
  },
};

export const Secondary: Story = {
  args: {
    children: 'زر ثانوي',
    variant: 'secondary',
    size: 'md',
  },
};

export const Outline: Story = {
  args: {
    children: 'زر محيطي',
    variant: 'outline',
    size: 'md',
  },
};

export const Ghost: Story = {
  args: {
    children: 'زر شفاف',
    variant: 'ghost',
    size: 'md',
  },
};

export const Link: Story = {
  args: {
    children: 'زر رابط',
    variant: 'link',
    size: 'md',
  },
};

export const WithIcons: Story = {
  args: {
    children: 'زر مع أيقونات',
    variant: 'primary',
    size: 'md',
    leftIcon: '🚀',
    rightIcon: '✨',
  },
};

export const Loading: Story = {
  args: {
    children: 'جاري التحميل',
    variant: 'primary',
    size: 'md',
    isLoading: true,
  },
};

export const Disabled: Story = {
  args: {
    children: 'زر معطل',
    variant: 'primary',
    size: 'md',
    isDisabled: true,
  },
};

export const FullWidth: Story = {
  args: {
    children: 'زر بعرض كامل',
    variant: 'primary',
    size: 'md',
    isFullWidth: true,
  },
};

export const Small: Story = {
  args: {
    children: 'زر صغير',
    variant: 'primary',
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    children: 'زر كبير',
    variant: 'primary',
    size: 'lg',
  },
}; 