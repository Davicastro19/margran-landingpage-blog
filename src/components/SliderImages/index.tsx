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
      spaceBetween={30}
      centeredSlides={true}
      autoplay={{
        delay: 2000,
        disableOnInteraction: false,
      }}

      loop ={true}
      effect={'coverflow'}
      slidesPerGroup={1}
      slidesPerView={4}
      coverflowEffect={{
        rotate: 50,
        stretch: 0,
        depth: 24,
        modifier: 1,
        slideShadows: true,
      }}
      modules={[Autoplay,EffectCoverflow]}
      className="mySwiper"
    >
      <SwiperSlide ><Box w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/9b/96/d5/9b96d54e8e23ac6a32f22a343e26e09d.jpg' alt='' width={'full'} height={'200px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Carrara
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/76/ab/25/76ab25a9f9cf0636c14e303a02304b90.jpg' alt=''width={'full'} height={'200px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Marquina
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/60/c8/c9/60c8c95545002a54468ca8c8666b89e1.jpg' alt='' width={'full'} height={'200px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Ubatuba
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/40/fe/ec/40feece717a5c063b3c1da554e220572.jpg' alt='' width={'full'} height={'200px'}/>
         <Center>
          <Heading fontWeight='400' color={'white'}>
          São Gabriel
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/95/d0/e9/95d0e9c36d6dfe27176f4d1ed13b285f.jpg' alt='' width={'full'} height={'200px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Giallo 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/6a/2c/9b/6a2c9bc0c785358fdadd6d271180bdf0.jpg' alt=''width={'full'} height={'200px'}/>
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Kashmir 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/5d/41/df/5d41df413086b4091392e2eeee48f38f.jpg' alt='' width={'full'} height={'200px'} />
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Ornamental
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/02/12/02/021202020b5c05e68b8b54dcf9f32615.jpg' alt='' width={'full'} height={'200px'}/>
         <Center>
          <Heading fontWeight='400' color={'white'}>
          Giallo 
          </Heading>
        </Center>
</Box>
        </SwiperSlide>
        <SwiperSlide><Box  w={{base: '100%', md: '100%', lg: '70%' }}>
         <Image borderRadius='20px' src='https://i.pinimg.com/236x/30/4f/1c/304f1cc419c66ca9766494d88f2a2958.jpg' alt='' width={'full'} height={'200px'} />
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
