import React from "react";

export enum ButtonType {
  PRIMARY = 'primary',
  SECONDARY = 'secondary',
  TERTIARY = 'tertiary',
  LINK = 'LINK',
}

export type StylishButtonProps = {
  id?: string;
  className?: string;
  type?: ButtonType;
  rounded?: boolean;
  disabled?: boolean;
  children?: React.ReactNode;
  href?: string;
  onClick?: () => void;
}

export default function StylishButton(props: StylishButtonProps) {
  const classNameByType = {
    [ButtonType.PRIMARY]: `
      flex items-center w-fit
      px-4 py-2 font-semibold
      text-gray-200 dark:text-gray-300 fill-gray-200 dark:fill-gray-300
      bg-[#0055ff] dark:bg-[#18168c]
      border-[#0055ff] dark:border-[#18168c]
      border-solid border-2
      hover:text-white hover:dark:text-gray-100 hover:[&_svg]:fill-white dark:hover:[&_svg]:fill-gray-100
      hover:bg-[#1f48c8] hover:dark:bg-[#172dc9]
      border-[#1f48c8] dark:hover:border-[#172dc9]
      disabled:hover:text-gray-200 dark:disabled:hover:text-gray-300 disabled:hover[&_svg]:fill-gray-200 dark:disabled:hover[&_svg]:fill-gray-300
      disabled:hover:bg-[#0055ff] dark:disabled:hover:bg-[#18168c]
      disabled:hover:border-[#0055ff] dark:disabled:hover:border-[#18168c]
    `,
    [ButtonType.SECONDARY]: `
      flex items-center w-fit
      px-4 py-2 font-semibold
      border-solid border-2
      text-gray-600 dark:text-gray-400 [&_svg]:fill-gray-600 dark:[&_svg]:fill-gray-400
      border-gray-600 dark:border-gray-400
      hover:text-gray-800 dark:hover:text-gray-200 hover:[&_svg]:fill-gray-800 dark:hover:[&_svg]:fill-gray-200
      hover:border-gray-800 dark:hover:border-gray-200
      disabled:hover:text-gray-600 dark:disabled:hover:text-gray-400 [&_svg]:disabled:group-hover:fill-gray-600 dark:disabled:hover:[&_svg]:fill-gray-400
      disabled:hover:border-gray-600 dark:disabled:hover:border-gray-400 disabled:hover[&_svg]:fill-gray-600 dark:disabled:hover:[&_svg]:fill-gray-400
    `,
    [ButtonType.TERTIARY]: `
      flex items-center w-fit
      px-4 py-2 font-semibold
      border-hidden border-blue-600
      text-gray-600 dark:text-gray-400 [&_svg]:fill-gray-600 [&_svg]:dark:fill-gray-400
      border-gray-600 dark:border-gray-400
      hover:text-gray-800 dark:hover:text-gray-200 hover:[&_svg]:fill-gray-800 dark:hover:[&_svg]:fill-gray-200
      disabled:hover:text-gray-600 disabled:dark:hover:text-gray-400 disabled:hover[&_svg]:fill-gray-600 dark:disabled:hover[&_svg]:fill-gray-400
      hover:underline
      disabled:hover:no-underline
    `,
    [ButtonType.LINK]: `
      flex items-center w-fit
      font-semibold
      text-gray-600 dark:text-gray-400 [&_svg]:fill-gray-600 [&_svg]:dark:fill-gray-400
      hover:text-gray-800 dark:hover:text-gray-200 hover:[&_svg]:fill-gray-800 dark:hover:[&_svg]:fill-gray-200
      disabled:hover:text-gray-600 disabled:dark:hover:text-gray-400 disabled:hover[&_svg]:fill-gray-600 dark:disabled:hover[&_svg]:fill-gray-400
      hover:underline
      disabled:hover:no-underline
    `,
  };

  const className = [
    classNameByType[props.type ?? ButtonType.TERTIARY],
    props.rounded ? "rounded-full" : "",
    props.disabled ? "cursor-not-allowed" : "",
  ].join(" ");

  if (props.href) {
    return (
      <a
        id={props.id}
        className={className}
        href={props.href}
        onClick={props.onClick}
      >
        {props.children}
      </a>
    );
  }

  return (
    <button
      id={props.id}
      className={className}
      onClick={props.onClick}
      disabled={props.disabled}
    >
      {props.children}
    </button>
  );
}
