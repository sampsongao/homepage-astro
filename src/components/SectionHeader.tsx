export type SectionHeaderProps = {
  id: string;
  title: string;
  description: string;
  tag: string;
};

export default function SectionHeader(props: SectionHeaderProps) {
  return (
    <div id={props.id} className="text-left py-4">
      <div className="w-min px-2 py-1 mb-2 rounded-md text-gray-500 dark:text-gray-400 border border-solid border-gray-300 dark:border-gray-400">
        {props.tag}
      </div>

      <h1 className="text-3xl font-bold mb-2 text-black dark:text-white">
        {props.title}
      </h1>

      <p className="text-md text-gray-700 dark:text-gray-300">
        {props.description}
      </p>
    </div>
  );
}
