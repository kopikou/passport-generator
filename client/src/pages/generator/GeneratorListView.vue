<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";

const generatorViewStore = useGeneratorViewStore();

const{
  cafData,
}=storeToRefs(generatorViewStore)

import {computed, onBeforeMount, ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {GeneratorListData} from "src/types";
import {useRouter} from "vue-router";
import {storeToRefs} from "pinia";
import _ from "lodash";

const $q = useQuasar()
const router = useRouter()
const listData = ref<GeneratorListData[]>([])

async function getProgramData() {
  let r = await api.get("api/generator/get-program-list/")
  listData.value = r.data
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

onBeforeMount(async () => {
  $q.loading.show()
  await getProgramData()
  $q.loading.hide()
})

</script>

<template>
  <div class="q-pa-lg">
    <div class="text-center text-h6 q-mb-md">Список рабочих программ дисциплин ИРНИТУ</div>
    <div class="rpd-container">
      <div class="rpd-row rpd-row__header text-weight-bold">
        <div>Аббревиатура</div>
        <div>Код</div>
        <div>Дисциплина</div>
        <div>Составитель</div>
        <div>Кафедра</div>
        <div>Статус</div>
      </div>
      <div class="rpd-row rpd-row__body" v-for="item in listData" @click="router.push(`/generator/${item.id}/main`)">
        <div>{{ item.abbr }} {{ item.yr }}</div>
        <div>{{ item.discode }}</div>
        <div>{{ item.discpl }}</div>
        <div>{{ item.person }}</div>
        <div>{{ cafDataById[item.kafcode]?.label }}</div>
        <div>{{ item.status_verbose }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.rpd-container {
  display: grid;
  grid-template-columns: auto auto repeat(3, 1fr) auto;
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
