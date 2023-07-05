import { Box, Center, Divider, Heading } from "@chakra-ui/react";
import { motion } from "framer-motion";


export default function IconMove({iconRigth, iconLeft}: any) {
return (
    
                <Center marginTop='10%' justifyContent={'space-between'} w='80%' h='80px' bg='white' flexDir='row'>
                <motion.div  initial={{ marginLeft: 0 }}
            whileHover={{ marginLeft: '10px' }}
            transition={{ duration: 0.3 }}>
      <Box position="relative" display="inline-block">
        <Box
          position="absolute"
          top="-15px"
          left="-10px"
          width="60px"
          height="60px"
          borderRadius="50%"
          backgroundColor="var(--primary)"
        >
          <motion.div
            initial={{ marginLeft: 0 }}
            whileHover={{ marginLeft: '20px' }}
            transition={{ duration: 0.3 }}
          >
            {iconLeft}
          </motion.div>
        </Box>
      </Box>
    </motion.div>
                 {iconRigth}
                </Center>
                )}