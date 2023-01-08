let grids = [...document.querySelectorAll('.grid--masonry')];

if (grids.length && getComputedStyle(grids[0]).gridTemplateRows !== 'masonry') {
    grids = grids.map(grid => ({
        _el: grid,
        gap: parseFloat(getComputedStyle(grid).gridRowGap),
        items: [...grid.childNodes].filter(c => c.nodeType === 1 && +getComputedStyle(c).gridColumnEnd !== -1),
        ncol: 0,
        mod: 0
    }));

    function layout() {
        grids.forEach(grid => {
            /* get the post relayout number of columns */
            let ncol = getComputedStyle(grid._el).gridTemplateColumns.split(' ').length;

            grid.items.forEach(c => {
                let new_h = c.getBoundingClientRect().height;

                if (new_h !== +c.dataset.h) {
                    c.dataset.h = new_h;
                    grid.mod++
                }
            });

            /* if the number of columns has changed */
            if (grid.ncol !== ncol || grid.mod) {
                /* update number of columns */
                grid.ncol = ncol;

                /* revert to initial positioning, no margin */
                grid.items.forEach(c => c.style.removeProperty('margin-top'));

                console.log('penis')
                /* if we have more than one column */
                if (grid.ncol > 1) {
                    grid.items.slice(ncol).forEach((c, i) => {
                        let prev_fin = grid.items[i].getBoundingClientRect().bottom /* bottom edge of item above */,
                            curr_ini = c.getBoundingClientRect().top /* top edge of current item */;

    
                        c.style.marginTop = `${prev_fin + grid.gap - curr_ini}px`
                    })
                }

                grid.mod = 0
            }
        })
    }

    addEventListener('load', e => {
        layout(); /* initial load */
        addEventListener('resize', layout, false) /* on resize */
    }, false);
}