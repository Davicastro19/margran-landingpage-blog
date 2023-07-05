import { Box, Link, Flex, Button, useDisclosure, Collapse, Center } from '@chakra-ui/react';
import { useRouter } from 'next/router';
import { RxHamburgerMenu } from 'react-icons/rx';
import { AiOutlineClose } from 'react-icons/ai';
import {BsArrowRight} from 'react-icons/bs'
import logo from '../../../public/logo.svg';
import Image from 'next/image'
type NavLinkProps = {
  href: string;
  children: React.ReactNode;
};

export default function Header() {
  const { isOpen, onToggle } = useDisclosure();
  const router = useRouter();

  return (
    <Center  flexDir='column'   py={6} px={{ base: 4, md: 8 }}  justifyContent="space-between"  >
      <Flex w={'full'}  justifyContent="space-between" >
        <Link   href="/">
          <Image src={logo} alt="Logo" width={200}  />
        </Link>

        <Box marginTop="2%"  display={{ base: 'block', md: 'block', lg:'none' }}>
          <Button onClick={onToggle} variant="ghost" color="black" _hover={{ color: 'black.100' }}>
            {isOpen ? <AiOutlineClose color="black" /> : <RxHamburgerMenu />}
          </Button>
        </Box>
        {!isOpen  &&
        <Box w="40%"  display={{ base: 'none', md: 'none', lg:'flex' }}>
          <NavLinks activeLinkColor="cyan.500" />
        </Box>}
      </Flex>

      <Collapse in={isOpen}   animateOpacity>
        <Box  w='full'>
          <NavLinks activeLinkColor="cyan.500" />
        </Box>
      </Collapse>
    </Center>
  );
}

function NavLinks({ activeLinkColor }: { activeLinkColor: string }) {
  const router = useRouter();

  return (
    <Center justifyContent="space-between" w='full' flexDir={{ base: 'column', md: 'column' , lg:'row'}}>
      
        <Center >
          <NavLink href="/" outLink={false}isActive={router.pathname === '/'} >
            HOME
          </NavLink>
        </Center>
        <Center  >
          <NavLink href="/posts" outLink={false} isActive={router.pathname === '/posts'} >
            BLOG
          </NavLink>
        </Center>
        <Center   >
          <NavLink href="/sobre" outLink={false} isActive={router.pathname === '/quem-somos'} >
            SOBRE NÓS
          </NavLink>
        </Center>
        
        <Center >
          <NavLink href="/sobre" outLink={false}  isActive={router.pathname === '/quem-somos'}>
          FAQ
          </NavLink>
        </Center>
        <Center padding='14px 18px 14px 18px' flexDir={'row'} bg='#30373f' >
          <NavLink href="/sobre"   outLink={true} isActive={router.pathname === '/quem-somos'} >
            CONTATE-NOS 
          </NavLink>
          <BsArrowRight color='white'/>
        </Center>
      
    </Center>
  );
}

function NavLink({ href, children, isActive, outLink }: NavLinkProps & { isActive: boolean; outLink: boolean }) {
  
  

  return (
    <Link href={href} style={{textDecoration:  'none'}}  layerStyle={'noneline'} >
      <Box as="span"  borderBottomColor={isActive?'Black':'transparent'}   borderBottomWidth={'2px'}  color={outLink ?'white':'black'} fontSize="md" fontWeight="medium" mx={2}>
        {children}
      </Box>
    </Link>
  );
}
