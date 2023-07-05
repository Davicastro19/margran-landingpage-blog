import { Box, Center, Heading, Image } from "@chakra-ui/react";
import { motion } from "framer-motion";

export default function BodyBanner() {
  return (
    <Box  position="relative" >
      <Box position="relative" overflow="hidden">
        <Image  src={'/gifhomee.gif'} alt="Imagem" />

        <Box
          position="absolute"
          top={0}
          left={0}
          right={0}
          bottom={0}
          bg="rgba(0, 0, 0, 0.4)"
          zIndex={2}
          _after={{
            content: '""',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
          }}
        >
            
          <Center h="100%" flexDir="column">
          <motion.div
              initial={{ y: 100 }}
              animate={{ y: 0 }}
              transition={{ duration: 1 }}
            >
          <Center flexDir="row">
           
            <Box w='30px' h='1px' bg='var(--primary)'  />
           
            <Heading padding={'0px 10px 0px 10px'} fontWeight={'500'} size={{ base: 'sx', md: 'xs', lg: 'md' }} color='var(--primary)'>
              BEM-VINDO À MARGRAN DIGITAL 
            </Heading>
            <Box w='30px' h='1px' bg='var(--primary)' />
            </Center>
            </motion.div>
            <motion.div
              initial={{ y: 100 }}
              animate={{ y: 0 }}
              transition={{ duration: 1 }}
            >
            <Heading color='white' fontWeight={'500'}  fontSize={{ base: '28px', md: '50px', lg: '70px' }} >
              Painéis de Pedra
            </Heading>
            </motion.div>
            <motion.div
              initial={{ y: 100 }}
              animate={{ y: 0 }}
              transition={{ duration: 1 }}
            >
            <Heading color='white' fontWeight={'500'} fontSize={{ base: '28px', md: '50px', lg: '70px' }} >
              Natural de Alto Desempenho
            </Heading>
            </motion.div>
          </Center>
         
        </Box>
      </Box>
    </Box>
  );
}
