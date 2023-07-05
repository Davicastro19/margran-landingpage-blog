import React, { useRef, useState } from 'react';
// Import Swiper React components
import { Swiper, SwiperSlide } from 'swiper/react';

// Import Swiper styles
import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';

import 'swiper/css/effect-coverflow';
// import required modules
import { Autoplay, EffectCoverflow } from 'swiper/modules';
import { Box, Heading, Image ,Center} from '@chakra-ui/react';

export default function SliderImages() {
  return (
    <>
    <Swiper
      spaceBetween={0}
      centeredSlides={true}
      autoplay={{
        delay: 2000,
        disableOnInteraction: false,
      }}

      loop ={true}
      slidesPerGroup={1}
      slidesPerView={3}
     
      modules={[Autoplay]}
      className="mySwiper"
    >
      <SwiperSlide ><Box w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/a7/1f/61/a71f61e955a44e12bbe6a519e6f84100.jpg' alt='' width={'full'} height={'400px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Carrara
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/24/db/7a/24db7af4b3dcebb073140f4572b7bff1.jpg' alt=''width={'full'} height={'400px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Marquina
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/19/6e/97/196e97597c73d7d3b327059c32b9e565.jpg' alt='' width={'full'} height={'400px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Ubatuba
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/4a/0c/11/4a0c117cfafadb104d6a7ab42f023e06.jpg' alt='' width={'full'} height={'400px'}/>
         <Center>
          <Heading fontWeight='400' color={'white'}>
          São Gabriel
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/eb/a7/d5/eba7d5a20967cc9c89b30ba3b4fe1cfe.jpg' alt='' width={'full'} height={'400px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Giallo 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/736x/e0/63/d3/e063d374a70512c103f2f90996cfadff.jpg' alt=''width={'full'} height={'400px'}/>
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Kashmir 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/95/78/0d/95780dcf86c906fd3bbabd7093e1865d.jpg' alt='' width={'full'} height={'400px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Ornamental
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/ee/5b/ec/ee5bec11d2d0db563df5168d0e17e8c9.jpg' alt='' width={'full'} height={'400px'}/>
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Giallo 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='0px' src='https://i.pinimg.com/236x/c6/66/80/c666802e589e29632c9ef18184057ead.jpg' alt='' width={'full'} height={'400px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Azul 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
    </Swiper>
  </>
  );
}
