$(function () {
  $("form").submit(function () {
    return false;
  });
});

$( ".logo" ).click(function() {
  $( "#sidebar" ).toggle();
});

function debounce(fn, threshold) {
  var timeout;
  threshold = threshold || 600;
  return function debounced() {
    clearTimeout(timeout);
    var args = arguments;
    var _this = this;

    function delayed() {
      fn.apply(_this, args);
    }
    timeout = setTimeout(delayed, threshold);
  };
}

function matchApp(app, searchValue) {
  if (searchValue == "") {
    $(app).each(function () {
      $(this).show()
    })
  } else {
    $(app).hide()
    $(app).each(function () {
      if ($(this).find(".content").text().toLocaleLowerCase().includes(searchValue)) {
        $(this).show()
      }
    })
  }
}

$('#search').keyup(debounce(function () {
  //app.hide();
  let searchValue = $('#search').val().toLocaleLowerCase()
  matchApp(app, searchValue)
}, 1200));

$(document).ready(function () {
  app = $("main div .app");
  let lazyImages = [].slice.call(document.querySelectorAll("img.lazyload"));
  let active = false;

  const lazyLoad = function() {
    if (active === false) {
      active = true;

      setTimeout(function() {
        lazyImages.forEach(function(lazyImage) {
          if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== "none") {
            lazyImage.src = lazyImage.dataset.src;
            lazyImage.classList.remove("lazyload");

            lazyImages = lazyImages.filter(function(image) {
              return image !== lazyImage;
            });

            if (lazyImages.length === 0) {
              document.removeEventListener("scroll", lazyLoad);
              window.removeEventListener("resize", lazyLoad);
              window.removeEventListener("orientationchange", lazyLoad);
            }
          }
        });

        active = false;
      }, 200);
    }
  };

  document.addEventListener("scroll", lazyLoad);
  window.addEventListener("resize", lazyLoad);
  window.addEventListener("orientationchange", lazyLoad);
});