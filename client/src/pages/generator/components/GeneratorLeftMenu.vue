<script setup lang="ts">

const props = defineProps({
  id: {
    required: true,
  }
})

</script>

<template>
  <q-list
    bordered
    separator
    style="width: 95%;"
  >
    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/main`"
    >
      <q-item-section>
        <q-item-label>Титульный лист</q-item-label>
        <q-item-label caption>Основная информация о программе</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/competences`"
    >
      <q-item-section>
        <q-item-label>Компетенции</q-item-label>
        <q-item-label caption>Информация о компетенция программы</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/indicators`"
    >
      <q-item-section>
        <q-item-label>Индикаторы</q-item-label>
        <q-item-label caption>Информация об индикаторах программы</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/discipline-place`"
    >
      <q-item-section>
        <q-item-label>Место дисциплины в структуре ООП</q-item-label>
        <q-item-label caption></q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/structure`"
    >
      <q-item-section>
        <q-item-label>Структура дисциплины</q-item-label>
        <q-item-label caption>Информация о структуре дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/discipline-theme`"
    >
      <q-item-section>
        <q-item-label>Содержание тем дисциплины</q-item-label>
        <q-item-label caption>Информация о темах дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/discipline-lab`"
    >
      <q-item-section>
        <q-item-label>Содержание лабораторных работ</q-item-label>
        <q-item-label caption>Информация о лабораторных работах дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/discipline-practice`"
    >
      <q-item-section>
        <q-item-label>Содержание практических работ</q-item-label>
        <q-item-label caption>Информация о практических работах дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/discipline-independent`"
    >
      <q-item-section>
        <q-item-label>Содержание самостоятельных работ</q-item-label>
        <q-item-label caption>Информация о самостоятельных работах дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/library`"
    >
      <q-item-section>
        <q-item-label>Литература</q-item-label>
        <q-item-label caption>Информация об учебной литературе дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/rdw`"
    >
      <q-item-section>
        <q-item-label>Использованные результаты НИОКР</q-item-label>
        <q-item-label caption>Информация об НИОКР, используемые в дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/soft`"
    >
      <q-item-section>
        <q-item-label>Использованное программное обеспечение</q-item-label>
        <q-item-label caption>Информация об ПО, используемые в дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

    <q-item
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${props.id}/logistics`"
    >
      <q-item-section>
        <q-item-label>Используемое материально-техническое обеспечение</q-item-label>
        <q-item-label caption>Информация об МТО, используемые в дисциплины</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

  </q-list>
</template>

<style scoped>

</style>
