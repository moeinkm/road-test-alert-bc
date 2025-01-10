import type { ComponentType } from 'react';
import type { SVGProps } from 'react';

export type IconType = ComponentType<SVGProps<SVGSVGElement>>;

export interface NavigationItem {
  name: string;
  href: string;
  icon: IconType;
  activeIcon: IconType;
}