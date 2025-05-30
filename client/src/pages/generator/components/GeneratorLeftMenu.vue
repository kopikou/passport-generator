<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import {api} from "boot/axios";
import {computed} from "vue";
import _ from "lodash";
import useMainStore from "stores/mainStore";
import dayjs from "dayjs";

const props = defineProps({
  id: {
    required: true,
  }
})

const $q = useQuasar()

const mainStore = useMainStore();

const {
  FORCE_SCRIPT_NAME,
} = storeToRefs(mainStore)

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  statusVerbose,
  comment,
  disabled,
  rpdData,
  admissionData,
  planlinesData,
  errors,
  lekcHours,
  srsHours,
  prHours,
  labHours,
  hasTat,
} = storeToRefs(generatorViewStore)

const menuItems = computed(() => {
  let items = [];
  items.push(...[
      // title (название), url (ссылка), allow (cadmkind, отображать)
      {title: 'Титульный лист', url: 'main', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true},
      {title: 'Компетенции', url: 'competences', allow: [1, 2, 3, 4], rpd: true, rpp: true},
      {title: 'Индикаторы', url: 'indicators', allow: [1, 2, 3, 4], rpd: true, rpp: true},
      {title: 'Результаты освоения программы', url: 'competences', allow: [5], rpd: true, rpp: true},
      {title: 'Результаты освоения дисциплины ', url: 'indicators', allow: [5], rpd: true, rpp: true},
      {title: 'Место дисциплины в структуре ООП', url: 'discipline-place', allow: [1, 2, 3, 4], rpd: true, rpp: false},
      {title: 'Структура дисциплины', url: 'structure', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true},
      {title: 'Содержание практики', url: 'practice-content', allow: [1, 2, 3, 4, 5], rpd: false, rpp: true},
      {title: 'Форма отчетности', url: 'practice-report', allow: [1, 2, 3, 4, 5], rpd: false, rpp: true},
      {title: 'Содержание тем дисциплины', url: 'discipline-theme', allow: [1, 2, 3, 4, 5], rpd: true, rpp: false},
    ]
  );

  if (lekcHours.value) {
    items.push({
      title: 'Содержание лекционных занятий',
      url: 'discipline-lectures',
      'right': true,
      allow: [1, 2, 3, 4, 5], rpd: true, rpp: false
    })
  }
  if (labHours.value) {
    items.push({title: 'Содержание лабораторных работ', url: 'discipline-lab', 'right': true, allow: [1, 2, 3, 4, 5], rpd: true, rpp: false})
  }
  if (prHours.value) {
    items.push({
      title: 'Содержание практических занятий',
      url: 'discipline-practice',
      'right': true,
      allow: [1, 2, 3, 4, 5], rpd: true, rpp: false
    })
  }
  if (srsHours.value) {
    items.push({
      title: 'Содержание самостоятельных работ',
      url: 'discipline-independent',
      'right': true,
      allow: [1, 2, 3, 4, 5], rpd: true, rpp: false
    })
  }


  items.push(...[
    {title: 'Перечень учебно-методического обеспечения', url: 'guidelines', allow: [1, 2, 3, 4, 5], rpd: true, rpp: false},
    {
      title: 'Оценочные материалы по дисциплине для контроля текущей успеваемости',
      url: 'fos',
      allow: [1, 2, 3, 4, 5], rpd: true, rpp: false
    },
  ])

  if (hasTat.value) {
    items.push({title: 'Типовые оценочные средства промежуточной аттестации', url: 'tat', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true});
  }

  items.push(...[
    {title: 'Литература', url: 'library', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true},
    {title: 'Другие ресурсы', url: 'resources', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true},
    {title: 'Перечень используемых информационных технологий', url: 'soft', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true},
    {title: 'Материально-техническое обеспечение', url: 'logistics', allow: [1, 2, 3, 4, 5], rpd: true, rpp: true},
  ]);

  return items;
});

const filterMenuItems = computed(() => {
   if (planlinesData.value.viewpract) {
    return _(menuItems.value).filter(x => x.allow.includes(admissionData.value.cadmkind)).filter(x => x.rpp).value()
  } else {
    return _(menuItems.value).filter(x => x.allow.includes(admissionData.value?.cadmkind)).filter(x => x.rpd).value()
  }
})

const criticalErrors = computed(() => {
  return _.filter(errors.value, x => x.level == 'critical')
})

function getUrl(url) {
  if (planlinesData.value.viewpract) {
    return `/practice_generator/${props.id}/${url}`
  } else {
    return `/generator/${props.id}/${url}`
  }
}

async function sendToReview() {
  $q.loading.show()
  let r = await api.get(`/api/generator/${activeRpdId.value}/send-rpd-on-review/`)
  rpdData.value.status = r.data.status
  rpdData.value.status_verbose = r.data.status_verbose
  $q.loading.hide()
}

function translateDate(date) {
  let result = dayjs(new Date(date)).format("DD MMMM YYYY в HH:mm")
  return result
}

function getErrors(url) {
  return _.filter(errors.value, x => x.url == url)
}


</script>

<template>
  <div style="display: grid; grid-template-rows: auto 1fr; overflow: hidden; height: 100%">
    <div class="q-pa-sm" v-if="comment?.comment">
      <q-expansion-item
        class="bg-blue-2"
        expand-separator
        icon="mdi-information"
        :label="`Комментарий от ${comment.user__last_name} ${comment.user__first_name}`"
        :caption="translateDate(comment.created_at)"
      >
        <q-card class="q-pa-sm bg-blue-1" style="max-height: 300px; overflow-y: auto">
          {{ comment.comment }}
        </q-card>
      </q-expansion-item>
      <!--      <div class="bg-pink-2 q-pa-sm rounded-borders" v-if="comment.length != 0">-->
      <!--        <div class="text-subtitle1">-->
      <!--          {{ comment.user__last_name }} {{ comment.user__first_name }}-->
      <!--          <small>оставил комментарий</small>-->
      <!--        </div>-->
      <!--        <div class="bg-grey-2 q-pa-sm rounded-borders" style="box-shadow: 0 0 4px silver inset">-->
      <!--              -->
      <!--        </div>-->
      <!--        <div class="text-right q-mt-sm" style="font-size: 0.7rem"></div>-->
      <!--      </div>-->
    </div>
    <q-list
      style="overflow-y: auto"
      bordered
      separator
    >
      <q-item
        v-for="item in filterMenuItems"
        clickable
        v-ripple
        active-class="bg-amber-2 text-black"
        :to="getUrl(item.url)"
        dense
        style="padding: 12px;"
      >
        <q-item-section>
          <q-item-label :class="item.right ? 'q-ml-lg' : ''">{{ item.title }}</q-item-label>
          <!--        <q-item-label caption>Основная информация о программе</q-item-label>-->
        </q-item-section>
        <q-item-section avatar v-if="getErrors(item.url).length != 0">
          <q-icon :name="getErrors(item.url)[0].level == 'warning' ? 'mdi-alert' : 'mdi-alert-box'"
                  :color="getErrors(item.url)[0].level == 'warning' ? 'amber-4' : 'red-7'">
            <q-tooltip class="text-white hide-scrollbar"
                       :class="getErrors(item.url)[0].level == 'warning' ? 'bg-amber-8' : 'bg-red-9'" max-height="20%">
              <div v-for="error in getErrors(item.url)" style="font-size: 14px;">
                <div v-for="text in error.text">
                  {{ text }}
                </div>
              </div>
            </q-tooltip>
          </q-icon>
        </q-item-section>
      </q-item>

    </q-list>

  </div>
</template>

<style scoped>

</style>
