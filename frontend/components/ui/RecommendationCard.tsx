import { motion } from 'framer-motion';
import Image from 'next/image';
import { twMerge } from 'tailwind-merge';
import { StarIcon, HeartIcon } from '@heroicons/react/solid';

interface RecommendationCardProps {
  title: string;
  description: string;
  imageUrl: string;
  rating: number;
  category: string;
  isFavorite?: boolean;
  onFavorite?: () => void;
  className?: string;
}

export const RecommendationCard = ({
  title,
  description,
  imageUrl,
  rating,
  category,
  isFavorite = false,
  onFavorite,
  className,
}: RecommendationCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      className={twMerge(
        'group relative overflow-hidden rounded-xl bg-white shadow-lg transition-all dark:bg-gray-800',
        className
      )}
    >
      <div className="relative h-48 w-full">
        <Image
          src={imageUrl}
          alt={title}
          layout="fill"
          objectFit="cover"
          className="transition-transform duration-300 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <button
          onClick={onFavorite}
          className="absolute top-2 right-2 rounded-full bg-white/20 p-2 backdrop-blur-sm transition-colors hover:bg-white/30"
        >
          <HeartIcon
            className={twMerge(
              'h-5 w-5',
              isFavorite
                ? 'text-red-500'
                : 'text-white group-hover:text-red-500'
            )}
          />
        </button>
      </div>

      <div className="p-4">
        <div className="mb-2 flex items-center justify-between">
          <span className="rounded-full bg-primary-100 px-2 py-1 text-xs font-medium text-primary-600 dark:bg-primary-900/20 dark:text-primary-400">
            {category}
          </span>
          <div className="flex items-center space-x-1">
            <StarIcon className="h-4 w-4 text-yellow-400" />
            <span className="text-sm font-medium text-gray-600 dark:text-gray-300">
              {rating.toFixed(1)}
            </span>
          </div>
        </div>

        <h3 className="mb-1 text-lg font-semibold text-gray-900 dark:text-white">
          {title}
        </h3>
        <p className="text-sm text-gray-600 line-clamp-2 dark:text-gray-400">
          {description}
        </p>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="mt-4 w-full rounded-lg bg-primary-600 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-700 dark:bg-primary-500 dark:hover:bg-primary-600"
        >
          عرض التفاصيل
        </motion.button>
      </div>
    </motion.div>
  );
}; 