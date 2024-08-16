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
      :to="`/generator/${props.id}/competences`"
    >
      <q-item-section>
        <q-item-label>Индикаторы</q-item-label>
        <q-item-label caption>Информация об индикаторах программы</q-item-label>
      </q-item-section>
      <q-item-section side top>
        <q-badge color="teal" label="Заполнено!"/>
      </q-item-section>
    </q-item>

  </q-list>
</template>

<style scoped>

</style>
