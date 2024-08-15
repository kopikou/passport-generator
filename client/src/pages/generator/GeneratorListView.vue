<script setup lang="ts">


import {onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";

const $q = useQuasar()
const listData = ref([])

async function getProgramData() {
  let r = await api.get("api/generator/get-program-list/")
  listData.value = r.data
}

onBeforeMount(async () => {
  $q.loading.show()
  await getProgramData()
  $q.loading.hide()
})

</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Генератор рабочих программ дисциплин ИРНИТУ</div>
    <div class="rpd-container">
      <div class="rpd-row rpd-row__header text-weight-bold">
        <div>Аббревиатура</div>
        <div>Код</div>
        <div>Дисциплина</div>
        <div>Составитель</div>
        <div>Кафедра</div>
        <div>Статус</div>
        <div></div>
      </div>
      <div class="rpd-row rpd-row__body">
        <div>АСУб 2024</div>
        <div>код дисциплины</div>
        <div>дисциплина</div>
        <div>Составитель</div>
        <div>кафедра</div>
        <div>статус</div>
        <div>Просмотр файлов</div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto auto repeat(3, 1fr) auto auto;
}

.rpd-row {
  display: contents;

  $border: solid 1px silver;

  > div {
    padding: 0.5rem;
    border: $border;
    border-right: none;
    border-bottom: none;

    &:last-child {
      border-right: $border;
    }
  }

  &:last-child {
    > div {
      border-bottom: $border;
    }
  }

  &.rpd-row__body {
    &:hover {
      > div {
        background: $pink-5;
        cursor: pointer;
      }
    }
  }

}

</style>
