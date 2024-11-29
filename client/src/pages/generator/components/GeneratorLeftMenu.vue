<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import {api} from "boot/axios";

const props = defineProps({
  id: {
    required: true,
  }
})

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  statusVerbose,
  comment,
  disabled,
} = storeToRefs(generatorViewStore)

const menuItems = [
  {title: 'Титульный лист', url: 'main'},
  {title: 'Компетенции', url: 'competences'},
  {title: 'Индикаторы', url: 'indicators'},
  {title: 'Место дисциплины в структуре ООП', url: 'discipline-place'},
  {title: 'Структура дисциплины', url: 'structure'},
  {title: 'Содержание тем дисциплины', url: 'discipline-theme'},
  {title: '->Содержание лекционных работ', url: 'discipline-lectures'},
  {title: '->Содержание лабораторных работ', url: 'discipline-lab'},
  {title: '->Содержание практических работ', url: 'discipline-practice'},
  {title: '->Содержание самостоятельных работ', url: 'discipline-independent'},
  {title: 'Методические указания', url: 'guidelines'},
  {title: 'Фонд оценочных средств', url: 'fos'},
  {title: 'Типовые оценочные средства', url: 'tat'},
  {title: 'Другие ресурсы', url: 'resources'},
  {title: 'Литература', url: 'library'},
  {title: 'Использованное программное обеспечение', url: 'soft'},
  {title: 'Используемое материально-техническое обеспечение', url: 'logistics'},
]

const $q = useQuasar()

async function sendToReview() {
  $q.loading.show()
  let r = await api.get(`/api/generator/${activeRpdId.value}/send-rpd-on-review/`)

  $q.loading.hide()
}


function translateDate(date) {
  let result = new Date(date).toLocaleString('ru')
  return result
}


</script>

<template>
  <q-list
    bordered
    separator
  >
    <q-item
      v-for="item in menuItems"
      clickable
      v-ripple
      active-class="bg-amber-4 text-black"
      :to="`/generator/${id}/${item.url}`"
      dense
      style="padding: 12px;"
    >
      <q-item-section>
        <q-item-label>{{ item.title }}</q-item-label>
        <!--        <q-item-label caption>Основная информация о программе</q-item-label>-->
      </q-item-section>
    </q-item>

  </q-list>
  <div>
    <div class="text-h6">Последний комментарий</div>
    <div>
      <div class="bg-grey-2 q-ma-xs text-subtitle1">
        <div v-if="comment.length != 0">
          <div class="text-subtitle1 text-bold">{{ translateDate(comment.created_at) }}</div>
          <div>
            {{ comment.comment }}
          </div>
        </div>
        <div v-else>
          <div class="text-subtitle text-bold">Комментариев нет</div>
        </div>
      </div>
    </div>
  </div>
  <div v-if="!disabled" class="q-mb-md">
    <q-btn
      class="q-mt-xs"
      color="secondary"
      dense
      @click="sendToReview"
      style="width: 100%"
      label="Отправить на согласование"
    />
  </div>
  <div v-else class="text-center q-mb-md">
    <q-btn
      class="q-mt-xs"
      color="secondary"
      dense
      disable
      style="width: 100%"
      :label="statusVerbose"
    />
  </div>


</template>

<style scoped>

</style>
