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
import { Box, Heading, Image ,Center, Text} from '@chakra-ui/react';

export default function SliderTestemonials() {
  return (
    <>
    <Swiper
      spaceBetween={0}
      centeredSlides={true}
      autoplay={{
        delay: 1500,
        disableOnInteraction: false,
      }}

      loop ={true}
      slidesPerGroup={1}
      slidesPerView={1}
     
      modules={[Autoplay]}
      className="mySwiper"
    >
      <SwiperSlide >
        <Center flexDir={'column'} w={'full'}>
        <Center flexDir={'column'} w={{base: '100%', md: '100%', lg: '70%' }}>
        <Text textAlign="center">A Marblex deve procurar por aqueles que sejam específicos, detalhados e destaquem os benefícios exclusivos de trabalhar com a empresa. Isso pode incluir aspectos como a qualidade dos produtos de mármore e um excelente atendimento ao cliente. A Marblex pode fazer essas avaliações para se diferenciar</Text>
        <Center flexDir={'column'} marginTop='3%'>
          <Heading fontWeight='500' color={'var(--secondary)'}>
          Jonatas Castro F
          </Heading>
          <Text fontWeight='500' color={'var(--primary)'}>ADMINISTRADOR</Text>
        
        </Center>
        </Center>
</Center>
        </SwiperSlide>
        <SwiperSlide >
        <Center flexDir={'column'} w={'full'}>
        <Center flexDir={'column'} w={{base: '100%', md: '100%', lg: '70%' }}>
        <Text textAlign="center">A Marblex deve procurar por aqueles que sejam específicos, detalhados e destaquem os benefícios exclusivos de trabalhar com a empresa. Isso pode incluir aspectos como a qualidade dos produtos de mármore e um excelente atendimento ao cliente. A Marblex pode fazer essas avaliações para se diferenciar</Text>
        <Center flexDir={'column'} marginTop='3%'>
          <Heading fontWeight='500' color={'var(--secondary)'}>
          Rogel Castro F
          </Heading>
          <Text fontWeight='500' color={'var(--primary)'}>EMPRESARIO</Text>
        
        </Center>
        </Center>
</Center>
        </SwiperSlide>
        <SwiperSlide >
        <Center flexDir={'column'} w={'full'}>
        <Center flexDir={'column'} w={{base: '100%', md: '100%', lg: '70%' }}>
        <Text textAlign="center">A Marblex deve procurar por aqueles que sejam específicos, detalhados e destaquem os benefícios exclusivos de trabalhar com a empresa. Isso pode incluir aspectos como a qualidade dos produtos de mármore e um excelente atendimento ao cliente. A Marblex pode fazer essas avaliações para se diferenciar</Text>
        <Center flexDir={'column'} marginTop='3%'>
          <Heading fontWeight='500' color={'var(--secondary)'}>
          Areli Castro F
          </Heading>
          <Text fontWeight='500' color={'var(--primary)'}>CONTADORA</Text>
        
        </Center>
        </Center>
</Center>
        </SwiperSlide>
        <SwiperSlide >
        <Center flexDir={'column'} w={'full'}>
        <Center flexDir={'column'} w={{base: '100%', md: '100%', lg: '70%' }}>
        <Text textAlign="center">A Marblex deve procurar por aqueles que sejam específicos, detalhados e destaquem os benefícios exclusivos de trabalhar com a empresa. Isso pode incluir aspectos como a qualidade dos produtos de mármore e um excelente atendimento ao cliente. A Marblex pode fazer essas avaliações para se diferenciar</Text>
        <Center flexDir={'column'} marginTop='3%'>
          <Heading fontWeight='500' color={'var(--secondary)'}>
          Melqui Castro F
          </Heading>
          <Text fontWeight='500' color={'var(--primary)'}>LOGISTA</Text>
        
        </Center>
        </Center>
</Center>
        </SwiperSlide>
    </Swiper>
  </>
  );
}
