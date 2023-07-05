import { Box, Center, Heading } from "@chakra-ui/react";
import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";

interface TextType {
  text: string;
  title: string;
  base: string;
  md: string;
  lg: string;
  colorTitle: string | undefined;
}
export default function PreTitle({ text, title,base, md, lg, colorTitle }: TextType) {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <Box marginTop={{ base: base, md: md, lg: lg}}>
      <motion.div
        ref={ref}
        initial={{ x: 400 }}
        animate={inView ? { x: 0 } : {}}
        transition={{ duration: 0.8 }}
      >
        <Center flexDir="row" justifyContent="flex-start" marginBottom="2%">
          <Box w="30px" h="1px" bg="var(--primary)" />
          <Heading padding="0px 10px 0px 10px" fontWeight="500" size="xs" color="var(--primary)">
            {text}
          </Heading>
        </Center>
        <Heading fontWeight="500" size={{ base: 'xl', md: 'lx', lg: '2xl' }} color={ colorTitle || "black"}>
          {title}
        </Heading>
      </motion.div>
    </Box>
  );
}
